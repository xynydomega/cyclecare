from datetime import date

from ..cycle_calculator import calculate_bleeding_duration

from .cycle_clock import CycleClock
from .phase_calculator import PhaseCalculator
from .phase_scheduler import PhaseScheduler
from .cycle_state import CycleState


class PeriodLogger:

    def generate_cycle_state(
        self,
        first_day,
        last_day,
        cycle_length,
        today=None
    ):

        if today is None:
            today = date.today()

        if last_day > today:
            raise ValueError("Last period day cannot be in the future.")

        if isinstance(cycle_length, bool) or not isinstance(cycle_length, int):
            raise TypeError("Cycle length must be an integer.")

        if not 1 <= cycle_length <= 100:
            raise ValueError("Cycle length must be between 1 and 100.")

        bleeding_duration = calculate_bleeding_duration(
            first_day,
            last_day
        )

        if bleeding_duration > cycle_length:
            raise ValueError(
                "Bleeding duration cannot exceed the cycle length."
            )

        clock = CycleClock.get_cycle_time(
            first_day,
            cycle_length,
            today
        )

        phase_result = PhaseCalculator.determine_phase(
            clock["cycle_day"],
            cycle_length,
            bleeding_duration
        )

        schedule = PhaseScheduler.build_schedule(
            first_day,
            cycle_length,
            bleeding_duration
        )

        next_transition = None

        if not clock["is_overdue"]:
            next_transition = PhaseScheduler.get_next_transition(
                schedule,
                today
            )

        state = CycleState(
            today=clock["today"],
            cycle_day=clock["cycle_day"],
            current_phase=phase_result["phase"],
            phase_confidence=phase_result["confidence"],
            first_day=first_day,
            last_day=last_day,
            bleeding_duration=bleeding_duration,
            cycle_length=cycle_length,
            next_period=clock["next_period"],
            days_until_next_period=clock["days_until_next_period"],
            is_overdue=clock["is_overdue"],
            next_phase=(
                next_transition["next_phase"]
                if next_transition else None
            ),
            next_phase_date=(
                next_transition["transition_date"]
                if next_transition else None
            ),
            days_until_phase_change=(
                next_transition["days_remaining"]
                if next_transition else None
            ),
            phase_schedule=schedule
        )

        return state
