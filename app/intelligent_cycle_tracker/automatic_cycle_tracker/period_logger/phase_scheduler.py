from datetime import timedelta

from .phase_calculator import PhaseCalculator


class PhaseScheduler:

    @staticmethod
    def build_schedule(first_day, cycle_length, bleeding_duration):

        if cycle_length < 15:
            return []

        ovulation_day = PhaseCalculator.estimate_ovulation_day(
            cycle_length
        )

        ovulation_start = max(1, ovulation_day - 1)
        ovulation_end = ovulation_day + 1

        ranges = [
            ("menstrual", 1, bleeding_duration),
            (
                "follicular",
                bleeding_duration + 1,
                ovulation_start - 1
            ),
            (
                "ovulation",
                max(bleeding_duration + 1, ovulation_start),
                ovulation_end
            ),
            (
                "luteal",
                max(bleeding_duration + 1, ovulation_end + 1),
                cycle_length
            )
        ]

        schedule = []

        for phase, start_day, end_day in ranges:

            if start_day > end_day:
                continue

            start_date = first_day + timedelta(days=start_day - 1)
            end_date = first_day + timedelta(days=end_day - 1)

            schedule.append({
                "phase": phase,
                "start_day": start_day,
                "end_day": end_day,
                "start_date": start_date,
                "end_date": end_date
            })

        return schedule

    @staticmethod
    def get_next_transition(schedule, today):

        for index, phase in enumerate(schedule):

            if phase["start_date"] > today:
                return {
                    "next_phase": phase["phase"],
                    "transition_date": phase["start_date"],
                    "days_remaining": (
                        phase["start_date"] - today
                    ).days
                }

        return None
