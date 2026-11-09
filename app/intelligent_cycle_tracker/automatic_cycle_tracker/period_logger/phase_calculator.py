from datetime import timedelta


class PhaseCalculator:

    @staticmethod
    def estimate_ovulation_day(cycle_length):
        if cycle_length < 15:
            return None

        return cycle_length - 14

    @staticmethod
    def determine_phase(
        cycle_day,
        cycle_length,
        bleeding_duration
    ):
        if cycle_length < 15:
            return {
                "phase": "unavailable",
                "confidence": "low_confidence"
            }

        if bleeding_duration < 1:
            raise ValueError("Bleeding duration must be positive.")

        if cycle_day < 1:
            raise ValueError("Cycle day must be positive.")

        ovulation_day = PhaseCalculator.estimate_ovulation_day(
            cycle_length
        )

        ovulation_start = max(1, ovulation_day - 1)
        ovulation_end = ovulation_day + 1

        if cycle_day > cycle_length:
            return {
                "phase": "period_overdue",
                "confidence": "low_confidence",
                "estimated_ovulation_day": ovulation_day
            }

        if cycle_day <= bleeding_duration:
            phase = "menstrual"

        elif cycle_day < ovulation_start:
            phase = "follicular"

        elif cycle_day <= ovulation_end:
            phase = "ovulation"

        else:
            phase = "luteal"

        return {
            "phase": phase,
            "confidence": "estimated",
            "estimated_ovulation_day": ovulation_day,
            "ovulation_window": (
                ovulation_start,
                ovulation_end
            )
        }
