from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class CyclePosition:
    cycle_number: int
    cycle_day: int
    cycle_start: date
    next_estimated_period: date
    is_estimated: bool


def calculate_cycle_position(
    last_period_start: date,
    cycle_length: int,
    today: date = None
) -> CyclePosition:
    """
    Calculate the user's current estimated cycle position.

    The next estimated cycle starts automatically when the
    expected cycle length has elapsed.

    The first cycle is anchored to the last recorded period.
    Subsequent cycles are estimates, not confirmed menstruation.
    """

    if today is None:
        today = date.today()

    if not isinstance(last_period_start, date) or not isinstance(today, date):
        raise TypeError("Dates must be datetime.date objects.")

    if isinstance(cycle_length, bool) or not isinstance(cycle_length, int):
        raise TypeError("Cycle length must be a whole number.")

    if not 1 <= cycle_length <= 100:
        raise ValueError("Cycle length must be between 1 and 100 days.")

    if today < last_period_start:
        raise ValueError("Today's date cannot be before the last period start date.")

    elapsed_days = (today - last_period_start).days

    completed_cycles = elapsed_days // cycle_length

    cycle_day = (elapsed_days % cycle_length) + 1

    cycle_start = last_period_start + timedelta(
        days=completed_cycles * cycle_length
    )

    next_estimated_period = cycle_start + timedelta(days=cycle_length)

    return CyclePosition(
        cycle_number=completed_cycles + 1,
        cycle_day=cycle_day,
        cycle_start=cycle_start,
        next_estimated_period=next_estimated_period,
        is_estimated=completed_cycles > 0
    )


def calculate_cycle_day(
    last_period_start: date,
    today: date = None
) -> int:
    """
    Backwards-compatible calculator for a single recorded cycle.
    """
    if today is None:
        today = date.today()

    if not isinstance(last_period_start, date) or not isinstance(today, date):
        raise TypeError("Dates must be datetime.date objects.")

    if today < last_period_start:
        raise ValueError("Today's date cannot be before the last period start date.")

    return (today - last_period_start).days + 1
