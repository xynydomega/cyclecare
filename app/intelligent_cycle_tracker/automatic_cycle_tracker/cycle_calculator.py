
from dataclasses import dataclass
from datetime import date


@dataclass
class CycleRecord:
    first_day: date
    last_day: date
    bleeding_duration: int
    cycle_length: int


def calculate_bleeding_duration(
    first_day: date,
    last_day: date
) -> int:
    """
    Calculate the total number of bleeding days.

    Both the first and last day are included.
    """

    if not isinstance(first_day, date) or not isinstance(last_day, date):
        raise TypeError("Dates must be datetime.date objects.")

    if last_day < first_day:
        raise ValueError(
            "Last day cannot be earlier than first day."
        )

    return (last_day - first_day).days + 1


def create_cycle_record(
    first_day: date,
    last_day: date,
    cycle_length: int
) -> CycleRecord:
    """
    Validate user information and create a cycle record.
    """

    if isinstance(cycle_length, bool) or not isinstance(cycle_length, int):
        raise TypeError("Cycle length must be a whole number.")

    if cycle_length <= 0:
        raise ValueError("Cycle length must be greater than zero.")

    bleeding_duration = calculate_bleeding_duration(
        first_day,
        last_day
    )

    return CycleRecord(
        first_day=first_day,
        last_day=last_day,
        bleeding_duration=bleeding_duration,
        cycle_length=cycle_length
    )
