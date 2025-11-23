export const ClassType = {
    Regular: "regular",
    Advanced: "advanced",
    Micro: "micro"
} as const;
export type ClassType = typeof ClassType[keyof typeof ClassType];

export const TeamBatteryStatus = {
    NotClassified: "not_classified",
    WaitingForInspectionCall: "waiting_for_inspection_call",
    CalledForInspection: "called_for_inspection",
    InInspection: "in_inspection",
    InFlightQueue: "in_flight_queue",
    Flying: "flying",
    PostFlightInspection: "post_flight_inspection",
    Flown: "flown"
} as const;
export type TeamBatteryStatus = typeof TeamBatteryStatus[keyof typeof TeamBatteryStatus];

export const CurrentFlightStatus = {
    CompetitionPaused: "competition_paused",
    ReadyToTakeoff: "ready_to_takeoff",
    Flying: "flying",
    FailedTakeoff: "failed_takeoff",
    InFlightFail: "in_flight_fail",
    LandingFail: "landing_fail",
    SuccessfulFlight: "successful_flight"
} as const;
export type CurrentFlightStatus = typeof CurrentFlightStatus[keyof typeof CurrentFlightStatus];

export interface Team {
    team_id: string;
    competition_id: number;
    name: string;
    country: string;
    state: string;
    university: string;
    class: ClassType;
    battery_status: TeamBatteryStatus;
}

export interface CurrentFlight {
    team: Team | null;
    status: CurrentFlightStatus;
}

export interface BatteryRounds {
    regular: number;
    advanced: number;
    micro: number;
}

export interface BatteryResult {
    team_id: string;
    placing: number;
    score: number;
}

export interface RoundResults {
    round_number: number;
    results: BatteryResult[];
}

export interface ReleasedBatteries {
    regular: RoundResults[];
    advanced: RoundResults[];
    micro: RoundResults[];
}
