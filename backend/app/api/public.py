from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, col
from app.api.deps import SessionDep
from app.models import Team, SystemState, BatteryPlacing, ClassType, CurrentFlightStatus

router = APIRouter()

def get_system_state(session: SessionDep) -> SystemState:
    state = session.get(SystemState, 1)
    if not state:
        # Initialize if not exists (should be done by seed, but safe fallback)
        state = SystemState(id=1)
        session.add(state)
        session.commit()
        session.refresh(state)
    return state

@router.get("/team_battery_status")
def get_team_battery_status(session: SessionDep):
    teams = session.exec(select(Team)).all()
    return [
        {
            "team_id": t.id,
            "year_id": t.year_id,
            "name": t.name,
            "country": t.country,
            "state": t.state,
            "university": t.university,
            "class": t.class_,
            "battery_status": t.battery_status
        }
        for t in teams
    ]

@router.get("/current_flight_status")
def get_current_flight_status(session: SessionDep):
    state = get_system_state(session)
    if state.current_status == CurrentFlightStatus.competition_paused or not state.current_team_id:
        return {"team": None, "status": state.current_status}

    team = session.get(Team, state.current_team_id)
    if not team:
        return {"team": None, "status": state.current_status} # Should not happen if integrity maintained

    return {
        "team": {
            "team_id": team.id,
            "year_id": team.year_id,
            "name": team.name,
            "country": team.country,
            "state": team.state,
            "university": team.university,
            "class": team.class_,
            "battery_status": team.battery_status
        },
        "status": state.current_status
    }

@router.get("/current_battery_round")
def get_current_battery_round(session: SessionDep):
    state = get_system_state(session)
    return {
        "regular": state.current_round_regular,
        "advanced": state.current_round_advanced,
        "micro": state.current_round_micro
    }

@router.get("/last_released_battery_round")
def get_last_released_battery_round(session: SessionDep):
    # This requires querying BatteryPlacing to find max round per class
    # Or maybe we store this in SystemState?
    # The prompt says "Return last round number that has official results released per class".
    # We can query distinct round_number from BatteryPlacing for each class and take max.

    def get_max_round(class_: ClassType) -> int:
        statement = select(BatteryPlacing.round_number).where(BatteryPlacing.class_ == class_).order_by(BatteryPlacing.round_number.desc())
        result = session.exec(statement).first()
        return result if result else 0

    return {
        "regular": get_max_round(ClassType.regular),
        "advanced": get_max_round(ClassType.advanced),
        "micro": get_max_round(ClassType.micro)
    }

@router.get("/data_released_batteries")
def get_data_released_batteries(session: SessionDep):
    # Return all placing results for all released rounds per class

    def get_results(class_: ClassType):
        # Get all results for this class
        results = session.exec(select(BatteryPlacing).where(BatteryPlacing.class_ == class_).order_by(BatteryPlacing.round_number, BatteryPlacing.placing)).all()

        # Group by round
        grouped = {}
        for r in results:
            if r.round_number not in grouped:
                grouped[r.round_number] = []
            grouped[r.round_number].append({
                "team_id": r.team_id,
                "placing": r.placing,
                "score": r.score
            })

        return [
            {"round_number": k, "results": v}
            for k, v in grouped.items()
        ]

    return {
        "regular": get_results(ClassType.regular),
        "advanced": get_results(ClassType.advanced),
        "micro": get_results(ClassType.micro)
    }
