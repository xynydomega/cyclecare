from dataclasses import dataclass
from datetime import date


@dataclass
class CycleState:

    today: date
    cycle_day: int
    current_phase: str
    phase_confidence: str

    first_day: date
    last_day: date

    bleeding_duration: int
    cycle_length: int

    next_period: date
    days_until_next_period: int
    is_overdue: bool

    next_phase: str | None
    next_phase_date: date | None
    days_until_phase_change: int | None

    phase_schedule: list
