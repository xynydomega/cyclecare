from dataclasses import dataclass


@dataclass
class PhaseResult:
    phase_name: str
    phase_stage: str
    display_name: str
    cycle_day: int
    phase_start_day: int
    phase_end_day: int
    days_remaining: int
    estimated_ovulation_day: int
    estimated: bool = True


def identify_phase(cycle_day, cycle_length, bleeding_duration):

    for value, name in [
        (cycle_day, "Cycle day"),
        (cycle_length, "Cycle length"),
        (bleeding_duration, "Bleeding duration")
    ]:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a whole number.")

    if cycle_day < 1:
        raise ValueError("Cycle day must be at least 1.")

    if not 1 <= cycle_length <= 100:
        raise ValueError("Cycle length must be between 1 and 100 days.")

    if not 1 <= bleeding_duration <= cycle_length:
        raise ValueError("Invalid bleeding duration.")

    ovulation_day = max(1, cycle_length - 14)
    ovulation_start = max(1, ovulation_day - 1)
    ovulation_end = min(cycle_length, ovulation_day + 1)

    def phase_for_day(day):

        if day <= bleeding_duration:
            return ("Follicular Phase", "Menstruating")

        # Once the expected cycle has elapsed, remain in
        # the luteal phase until a new period is actually logged.
        if day > cycle_length:
            return ("Luteal Phase", "Awaiting period log")

        if ovulation_start <= day <= ovulation_end:
            return ("Ovulatory Phase", "Estimated ovulation window")

        if day < ovulation_start:
            return ("Follicular Phase", "Post-menstruation")

        return ("Luteal Phase", "Post-ovulation")

    current_phase, current_stage = phase_for_day(cycle_day)

    phase_start = cycle_day
    phase_end = cycle_day

    while (
        phase_start > 1
        and phase_for_day(phase_start - 1)
        == (current_phase, current_stage)
    ):
        phase_start -= 1

    while (
        phase_end < cycle_day
        or (
            phase_end < cycle_length
            and phase_for_day(phase_end + 1)
            == (current_phase, current_stage)
        )
    ):
        if phase_end >= cycle_day:
            break
        phase_end += 1

    # For an overdue, unlogged cycle, keep the current
    # luteal phase visible through the actual current day.
    if cycle_day > cycle_length and current_phase == "Luteal Phase":
        phase_end = cycle_day

    return PhaseResult(
        phase_name=current_phase,
        phase_stage=current_stage,
        display_name=f"{current_phase} ({current_stage})",
        cycle_day=cycle_day,
        phase_start_day=phase_start,
        phase_end_day=phase_end,
        days_remaining=max(0, phase_end - cycle_day),
        estimated_ovulation_day=ovulation_day,
        estimated=True
    )
