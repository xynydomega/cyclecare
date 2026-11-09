import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from tkcalendar import DateEntry

from intelligent_cycle_tracker.automatic_cycle_tracker.cycle_calculator import (
    calculate_bleeding_duration,
    estimate_next_period
)


class CycleGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("CycleCare - Cycle Calculator")
        self.root.geometry("450x480")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        main = ttk.Frame(self.root, padding=25)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="Menstrual Cycle Calculator",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 25))

        # First day
        ttk.Label(
            main,
            text="First day of menstruation"
        ).pack(anchor="w")

        self.first_day = DateEntry(
            main,
            width=35,
            date_pattern="yyyy-mm-dd",
            maxdate=date.today()
        )
        self.first_day.pack(fill="x", pady=(5, 20))

        # Last day
        ttk.Label(
            main,
            text="Last day of menstruation"
        ).pack(anchor="w")

        self.last_day = DateEntry(
            main,
            width=35,
            date_pattern="yyyy-mm-dd",
            maxdate=date.today()
        )
        self.last_day.pack(fill="x", pady=(5, 20))

        # Cycle length
        ttk.Label(
            main,
            text="Your cycle length (days)"
        ).pack(anchor="w")

        self.cycle_length = tk.IntVar(value=28)

        self.cycle_spinner = ttk.Spinbox(
            main,
            from_=1,
            to=100,
            increment=1,
            textvariable=self.cycle_length,
            width=10,
            justify="center"
        )
        self.cycle_spinner.pack(anchor="w", pady=(5, 20))

        # Calculate button
        ttk.Button(
            main,
            text="Calculate",
            command=self.calculate
        ).pack(fill="x")

        # Results
        self.result = ttk.Label(
            main,
            text="Your results will appear here.",
            font=("Arial", 11, "bold"),
            justify="center"
        )
        self.result.pack(pady=25)

    def calculate(self):

        try:
            first = self.first_day.get_date()
            last = self.last_day.get_date()
            cycle_length = self.cycle_length.get()

            if not 1 <= cycle_length <= 100:
                raise ValueError(
                    "Cycle length must be between 1 and 100 days."
                )

            duration = calculate_bleeding_duration(
                first,
                last
            )

            next_period = estimate_next_period(
                first,
                cycle_length
            )

            self.result.config(
                text=(
                    f"Bleeding duration: {duration} days\n"
                    f"Cycle length: {cycle_length} days\n\n"
                    f"ESTIMATED NEXT PERIOD\n"
                    f"{next_period.strftime('%B %d, %Y')}"
                )
            )

        except (ValueError, TypeError, tk.TclError) as error:
            messagebox.showerror(
                "Invalid Information",
                str(error)
            )


if __name__ == "__main__":

    root = tk.Tk()
    app = CycleGUI(root)
    root.mainloop()
