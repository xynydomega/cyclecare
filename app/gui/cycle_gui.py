
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from intelligent_cycle_tracker.automatic_cycle_tracker.cycle_calculator import (
    calculate_bleeding_duration
)


class CycleGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("CycleCare - Cycle Calculator")
        self.root.geometry("400x320")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        # Main container
        main = ttk.Frame(self.root, padding=25)
        main.pack(fill="both", expand=True)

        # Heading
        ttk.Label(
            main,
            text="Menstrual Cycle Calculator",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))

        # First day
        ttk.Label(
            main,
            text="First day of menstruation (YYYY-MM-DD)"
        ).pack(anchor="w")

        self.first_day = ttk.Entry(main, width=35)
        self.first_day.pack(fill="x", pady=(5, 15))

        # Last day
        ttk.Label(
            main,
            text="Last day of menstruation (YYYY-MM-DD)"
        ).pack(anchor="w")

        self.last_day = ttk.Entry(main, width=35)
        self.last_day.pack(fill="x", pady=(5, 20))

        # Calculate button
        ttk.Button(
            main,
            text="Calculate Bleeding Duration",
            command=self.calculate
        ).pack(fill="x", pady=5)

        # Result
        self.result = ttk.Label(
            main,
            text="Bleeding duration: --",
            font=("Arial", 12, "bold")
        )
        self.result.pack(pady=20)

    def calculate(self):

        try:
            first = date.fromisoformat(
                self.first_day.get().strip()
            )

            last = date.fromisoformat(
                self.last_day.get().strip()
            )

            duration = calculate_bleeding_duration(
                first,
                last
            )

            self.result.config(
                text=f"Bleeding duration: {duration} days"
            )

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input",
                str(error) if str(error) else
                "Enter valid dates in YYYY-MM-DD format."
            )


if __name__ == "__main__":

    root = tk.Tk()

    app = CycleGUI(root)

    root.mainloop()
