from datetime import date, timedelta


class CycleClock:

    @staticmethod
    def get_cycle_time(first_day, cycle_length, today=None):
        if today is None:
            today = date.today()

        if today < first_day:
            raise ValueError("First period date cannot be in the future.")

        if isinstance(cycle_length, bool) or not isinstance(cycle_length, int):
            raise TypeError("Cycle length must be an integer.")

        if cycle_length <= 0:
            raise ValueError("Cycle length must be positive.")

        elapsed_days = (today - first_day).days
        cycle_day = elapsed_days + 1

        next_period = first_day + timedelta(days=cycle_length)
        days_until_next_period = (next_period - today).days

        return {
            "today": today,
            "cycle_day": cycle_day,
            "days_elapsed": elapsed_days,
            "next_period": next_period,
            "days_until_next_period": days_until_next_period,
            "is_overdue": days_until_next_period < 0
        }
