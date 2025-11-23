from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# Enums

class ClassType(str, Enum):
    regular = "regular"
    advanced = "advanced"
    micro = "micro"

class TeamBatteryStatus(str, Enum):
    not_classified = "not_classified"
    waiting_for_inspection_call = "waiting_for_inspection_call"
    called_for_inspection = "called_for_inspection"
    in_inspection = "in_inspection"
    in_flight_queue = "in_flight_queue"
    flying = "flying"
    post_flight_inspection = "post_flight_inspection"
    flown = "flown"

class CurrentFlightStatus(str, Enum):
    competition_paused = "competition_paused"
    ready_to_takeoff = "ready_to_takeoff"
    flying = "flying"
    failed_takeoff = "failed_takeoff"
    in_flight_fail = "in_flight_fail"
    landing_fail = "landing_fail"
    successful_flight = "successful_flight"

# Models

class TeamBase(SQLModel):
    year_id: int
    name: str
    country: str
    state: str
    university: str
    class_: ClassType = Field(alias="class") # 'class' is a reserved keyword
    battery_status: TeamBatteryStatus = Field(default=TeamBatteryStatus.not_classified)

class Team(TeamBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class BatteryBase(SQLModel):
    round_number: int
    class_: ClassType = Field(alias="class")
    datetime_start: datetime
    datetime_finish: Optional[datetime] = None

class Battery(BatteryBase, table=True):
    # Composite primary key logic or just ID?
    # Prompt says: "There are no global “battery IDs.” Everything is identified by (class, round_number)."
    # But SQLModel usually wants a primary key. We can use a composite primary key.
    class_: ClassType = Field(alias="class", primary_key=True)
    round_number: int = Field(primary_key=True)

class FlightBase(SQLModel):
    team_id: UUID = Field(foreign_key="team.id")
    round_number: int
    class_: ClassType = Field(alias="class")
    status: CurrentFlightStatus

class Flight(FlightBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class BatteryPlacingBase(SQLModel):
    team_id: UUID = Field(foreign_key="team.id")
    round_number: int
    class_: ClassType = Field(alias="class")
    placing: int
    score: float

class BatteryPlacing(BatteryPlacingBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # Surrogate key for simplicity

# User Model for Auth
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="admin")

# Audit Log
class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_email: str
    action: str
    details: str # JSON string or description
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SystemState(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    current_team_id: Optional[UUID] = Field(default=None, foreign_key="team.id")
    current_status: CurrentFlightStatus = Field(default=CurrentFlightStatus.competition_paused)

    current_round_regular: int = Field(default=1)
    current_round_advanced: int = Field(default=1)
    current_round_micro: int = Field(default=1)

