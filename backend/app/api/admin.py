from typing import Annotated, Optional
from uuid import UUID
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlmodel import select
import csv
import io
import json

from app.api.deps import SessionDep, AdminUser
from app.models import (
    SystemState, Team, AuditLog,
    CurrentFlightStatus, TeamBatteryStatus, ClassType, BatteryPlacing
)

router = APIRouter()

def log_action(session: SessionDep, user_email: str, action: str, details: dict):
    log = AuditLog(
        user_email=user_email,
        action=action,
        details=json.dumps(details)
    )
    session.add(log)

class CurrentFlightUpdate(BaseModel):
    team_id: Optional[UUID]
    status: CurrentFlightStatus

@router.patch("/current_flight")
def update_current_flight(
    update: CurrentFlightUpdate,
    session: SessionDep,
    admin: AdminUser
):
    state = session.get(SystemState, 1)
    if not state:
        state = SystemState(id=1)
        session.add(state)

    prev_team = str(state.current_team_id)
    prev_status = state.current_status

    state.current_team_id = update.team_id
    state.current_status = update.status
    session.add(state)

    log_action(session, admin.email, "update_current_flight", {
        "prev_team": prev_team,
        "prev_status": prev_status,
        "new_team": str(update.team_id),
        "new_status": update.status
    })
    session.commit()
    return {"status": "ok"}

class TeamBatteryStatusUpdate(BaseModel):
    battery_status: TeamBatteryStatus

@router.patch("/team/{team_id}/battery_status")
def update_team_battery_status(
    team_id: UUID,
    update: TeamBatteryStatusUpdate,
    session: SessionDep,
    admin: AdminUser
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    prev_status = team.battery_status
    team.battery_status = update.battery_status
    session.add(team)

    log_action(session, admin.email, "update_team_battery_status", {
        "team_id": str(team_id),
        "prev_status": prev_status,
        "new_status": update.battery_status
    })
    session.commit()
    return {"status": "ok"}

class CurrentBatteryRoundUpdate(BaseModel):
    class_: ClassType = Field(alias="class")
    round_number: int

    class Config:
        populate_by_name = True  # Allow both 'class' and 'class_'

@router.patch("/current_battery_round")
def update_current_battery_round(
    update: CurrentBatteryRoundUpdate,
    session: SessionDep,
    admin: AdminUser
):
    state = session.get(SystemState, 1)
    if not state:
        state = SystemState(id=1)
        session.add(state)

    prev_round = 0
    if update.class_ == ClassType.regular:
        prev_round = state.current_round_regular
        state.current_round_regular = update.round_number
    elif update.class_ == ClassType.advanced:
        prev_round = state.current_round_advanced
        state.current_round_advanced = update.round_number
    elif update.class_ == ClassType.micro:
        prev_round = state.current_round_micro
        state.current_round_micro = update.round_number

    session.add(state)

    log_action(session, admin.email, "update_current_battery_round", {
        "class": update.class_,
        "prev_round": prev_round,
        "new_round": update.round_number
    })
    session.commit()
    return {"status": "ok"}

@router.post("/battery_placing_upload")
async def upload_battery_placing(
    round_number: int,
    file: UploadFile,
    session: SessionDep,
    admin: AdminUser,
    class_: ClassType = Query(alias="class"),
):
    content = await file.read()
    decoded = content.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))

    # Validate headers
    if not reader.fieldnames or not all(k in reader.fieldnames for k in ["team_year_id", "placing", "score"]):
        raise HTTPException(status_code=400, detail="Invalid CSV headers. Expected: team_year_id, placing, score")

    new_placings = []
    for row in reader:
        try:
            team_year_id = int(row["team_year_id"])
            placing = int(row["placing"])
            score = float(row["score"])
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid data in row: {row}. Error: {e}")

        # Verify team exists by year_id and class
        statement = select(Team).where(Team.year_id == team_year_id, Team.class_ == class_)
        team = session.exec(statement).first()

        if not team:
             raise HTTPException(status_code=400, detail=f"Team not found for year_id: {team_year_id} and class: {class_}")

        new_placings.append(BatteryPlacing(
            team_id=team.id,
            round_number=round_number,
            class_=class_,
            placing=placing,
            score=score
        ))

    # Check if results already exist for this round/class?
    # Prompt says "Commit the entire set in a single transaction."
    # It doesn't say to overwrite or append. Assuming overwrite or just add.
    # Usually results are uploaded once. If re-uploaded, maybe delete old ones?
    # Let's delete old ones for this round/class to be safe and avoid duplicates.

    statement = select(BatteryPlacing).where(
        BatteryPlacing.class_ == class_,
        BatteryPlacing.round_number == round_number
    )
    existing = session.exec(statement).all()
    for e in existing:
        session.delete(e)

    for p in new_placings:
        session.add(p)

    log_action(session, admin.email, "upload_battery_placing", {
        "class": class_,
        "round_number": round_number,
        "rows_count": len(new_placings)
    })

    # Update SystemState if the uploaded round is greater than current
    state = session.get(SystemState, 1)
    if not state:
        state = SystemState(id=1)
        session.add(state)

    updated_state = False
    if class_ == ClassType.regular and round_number > state.current_round_regular:
        state.current_round_regular = round_number
        updated_state = True
    elif class_ == ClassType.advanced and round_number > state.current_round_advanced:
        state.current_round_advanced = round_number
        updated_state = True
    elif class_ == ClassType.micro and round_number > state.current_round_micro:
        state.current_round_micro = round_number
        updated_state = True

    if updated_state:
        session.add(state)

    session.commit()
    return {"status": "ok", "count": len(new_placings)}

class GenerateBatteryResultsRequest(BaseModel):
    class_: ClassType = Field(alias="class")
    round_number: Optional[int] = None

@router.post("/generate_battery_results")
def generate_battery_results(
    request: GenerateBatteryResultsRequest,
    session: SessionDep,
    admin: AdminUser
):
    # 1. Get current state
    state = session.get(SystemState, 1)
    if not state:
        state = SystemState(id=1)
        session.add(state)

    # Determine target round
    if request.round_number is not None:
        new_round = request.round_number
    else:
        current_round = 0
        if request.class_ == ClassType.regular:
            current_round = state.current_round_regular
        elif request.class_ == ClassType.advanced:
            current_round = state.current_round_advanced
        elif request.class_ == ClassType.micro:
            current_round = state.current_round_micro
        new_round = current_round + 1

    # 2. Get all teams for this class
    teams = session.exec(select(Team).where(Team.class_ == request.class_)).all()

    if not teams:
        return {"status": "no_teams", "message": f"No teams found in {request.class_} class"}

    # 3. Get previous scores if round > 1
    previous_scores = {}
    if new_round > 1:
        prev_round = new_round - 1
        prev_placings = session.exec(
            select(BatteryPlacing)
            .where(BatteryPlacing.class_ == request.class_)
            .where(BatteryPlacing.round_number == prev_round)
        ).all()
        for p in prev_placings:
            previous_scores[p.team_id] = p.score

    # 4. Generate random scores (Cumulative)
    import random

    team_scores = []
    for team in teams:
        prev_score = previous_scores.get(team.id, 0.0)

        # If it's the first round, base score.
        # If subsequent round, add increment.
        # Ensure score never decreases (increment >= 0)

        if new_round == 1:
            # Base score for round 1
            score = round(random.uniform(100.0, 400.0), 2)
        else:
            # Increment for subsequent rounds
            increment = round(random.uniform(0.0, 100.0), 2)
            score = prev_score + increment

        team_scores.append({"team": team, "score": score})

    # 5. Calculate placings
    # Sort by score descending
    team_scores.sort(key=lambda x: x["score"], reverse=True)

    # 6. Delete existing results for this round/class (Overwrite)
    existing_placings = session.exec(
        select(BatteryPlacing).where(
            BatteryPlacing.class_ == request.class_,
            BatteryPlacing.round_number == new_round
        )
    ).all()
    for e in existing_placings:
        session.delete(e)

    # 7. Create BatteryPlacing records
    new_placings = []
    for i, item in enumerate(team_scores):
        placing = i + 1
        new_placings.append(BatteryPlacing(
            team_id=item["team"].id,
            round_number=new_round,
            class_=request.class_,
            placing=placing,
            score=item["score"]
        ))

    # 8. Update SystemState (Always update to the generated round)
    if request.class_ == ClassType.regular:
        state.current_round_regular = new_round
    elif request.class_ == ClassType.advanced:
        state.current_round_advanced = new_round
    elif request.class_ == ClassType.micro:
        state.current_round_micro = new_round

    session.add(state)

    # 9. Save everything
    for p in new_placings:
        session.add(p)

    log_action(session, admin.email, "generate_battery_results", {
        "class": request.class_,
        "round": new_round,
        "teams_count": len(teams),
        "overwritten": len(existing_placings) > 0
    })

    session.commit()

    return {
        "status": "ok",
        "message": f"Generated results for round {new_round} with {len(teams)} teams",
        "new_round": new_round
    }
