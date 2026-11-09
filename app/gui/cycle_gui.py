import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from tkcalendar import DateEntry

from intelligent_cycle_tracker.automatic_cycle_tracker.cycle_calculator import (
    calculate_bleeding_duration
)

from intelligent_cycle_tracker.period_logger.cycle_day_calculator import (
    calculate_cycle_position
)

from intelligent_cycle_tracker.period_logger.phase_identifier import (
    identify_phase
)


class CycleGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("CycleCare - Cycle Calculator")
        self.root.geometry("500x700")
        self.root.minsize(400, 450)

        self.create_widgets()

    def create_widgets(self):

        # Scrollable interface container
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        main = ttk.Frame(canvas, padding=25)

        window_id = canvas.create_window(
            (0, 0),
            window=main,
            anchor="nw"
        )

        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def resize_main(event):
            canvas.itemconfigure(window_id, width=event.width)

        main.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", resize_main)

        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        ttk.Label(
            main,
            text="Menstrual Cycle Calculator",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))

        ttk.Label(
            main,
            text="First day of last recorded menstruation"
        ).pack(anchor="w")

        self.first_day = DateEntry(
            main,
            width=35,
            date_pattern="yyyy-mm-dd",
            maxdate=date.today()
        )
        self.first_day.pack(fill="x", pady=(5, 12))

        ttk.Label(
            main,
            text="Last day of that menstruation"
        ).pack(anchor="w")

        self.last_day = DateEntry(
            main,
            width=35,
            date_pattern="yyyy-mm-dd",
            maxdate=date.today()
        )
        self.last_day.pack(fill="x", pady=(5, 12))

        ttk.Label(
            main,
            text="Expected cycle length (days)"
        ).pack(anchor="w")

        self.cycle_length = tk.IntVar(value=28)

        ttk.Spinbox(
            main,
            from_=1,
            to=100,
            increment=1,
            textvariable=self.cycle_length,
            width=10,
            justify="center"
        ).pack(anchor="w", pady=(5, 12))

        # Period logging
        log_frame = ttk.LabelFrame(
            main,
            text="PERIOD LOGGING",
            padding=10
        )
        log_frame.pack(fill="x", pady=10)

        self.period_logged = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            log_frame,
            text="I have logged a new period",
            variable=self.period_logged
        ).pack(anchor="w")

        ttk.Label(
            log_frame,
            text="New period start date"
        ).pack(anchor="w", pady=(8, 0))

        self.new_period_date = DateEntry(
            log_frame,
            width=35,
            date_pattern="yyyy-mm-dd",
            maxdate=date.today()
        )
        self.new_period_date.pack(fill="x", pady=(5, 0))

        ttk.Button(
            main,
            text="Calculate",
            command=self.calculate
        ).pack(fill="x", pady=10)

        # Current cycle day
        current_frame = ttk.LabelFrame(
            main,
            text="CURRENT CYCLE DAY",
            padding=12
        )
        current_frame.pack(fill="x", pady=7)

        self.current_day_label = ttk.Label(
            current_frame,
            text="--",
            font=("Arial", 28, "bold"),
            anchor="center"
        )
        self.current_day_label.pack(fill="x")

        self.current_day_description = ttk.Label(
            current_frame,
            text="",
            font=("Arial", 10),
            anchor="center"
        )
        self.current_day_description.pack(fill="x", pady=3)

        self.logged_status = ttk.Label(
            current_frame,
            text="",
            font=("Arial", 10, "bold"),
            anchor="center"
        )
        self.logged_status.pack(fill="x")

        # Estimated cycle day
        estimated_frame = ttk.LabelFrame(
            main,
            text="ESTIMATED CYCLE DAY",
            padding=12
        )
        estimated_frame.pack(fill="x", pady=7)

        self.estimated_day_label = ttk.Label(
            estimated_frame,
            text="--",
            font=("Arial", 28, "bold"),
            anchor="center"
        )
        self.estimated_day_label.pack(fill="x")

        self.estimated_description = ttk.Label(
            estimated_frame,
            text="",
            font=("Arial", 10),
            anchor="center"
        )
        self.estimated_description.pack(fill="x", pady=3)

        self.estimated_date_label = ttk.Label(
            estimated_frame,
            text="",
            font=("Arial", 9),
            anchor="center"
        )
        self.estimated_date_label.pack(fill="x")

        # Estimated cycle phase
        phase_frame = ttk.LabelFrame(
            main,
            text="CYCLE PHASE",
            padding=12
        )
        phase_frame.pack(fill="x", pady=7)

        self.phase_name_label = ttk.Label(
            phase_frame,
            text="--",
            font=("Arial", 17, "bold"),
            anchor="center"
        )
        self.phase_name_label.pack(fill="x", pady=4)

        self.phase_stage_label = ttk.Label(
            phase_frame,
            text="",
            font=("Arial", 10),
            anchor="center"
        )
        self.phase_stage_label.pack(fill="x", pady=3)

        self.phase_days_label = ttk.Label(
            phase_frame,
            text="",
            font=("Arial", 10),
            anchor="center"
        )
        self.phase_days_label.pack(fill="x", pady=3)

        self.phase_estimate_label = ttk.Label(
            phase_frame,
            text="Phase information is estimated.",
            font=("Arial", 9),
            anchor="center"
        )
        self.phase_estimate_label.pack(fill="x", pady=3)

        # Cycle information
        info_frame = ttk.LabelFrame(
            main,
            text="CYCLE INFORMATION",
            padding=10
        )
        info_frame.pack(fill="x", pady=7)

        self.info_label = ttk.Label(
            info_frame,
            text="Your cycle information will appear here.",
            font=("Arial", 10),
            justify="center"
        )
        self.info_label.pack()

        # Guidance
        guidance_frame = ttk.LabelFrame(
            main,
            text="CYCLECARE GUIDANCE",
            padding=10
        )
        guidance_frame.pack(fill="x", pady=7)

        self.guidance_label = ttk.Label(
            guidance_frame,
            text=""
        )
        self.guidance_label.pack()

    def calculate(self):

        try:
            first = self.first_day.get_date()
            last = self.last_day.get_date()
            today = date.today()
            cycle_length = self.cycle_length.get()

            if not 1 <= cycle_length <= 100:
                raise ValueError(
                    "Cycle length must be between 1 and 100 days."
                )

            duration = calculate_bleeding_duration(first, last)

            if last > today:
                raise ValueError(
                    "Last menstruation date cannot be in the future."
                )

            logged = self.period_logged.get()

            if logged:
                new_start = self.new_period_date.get_date()

                if new_start < first:
                    raise ValueError(
                        "New period date cannot be before the previous period."
                    )

                if new_start > today:
                    raise ValueError(
                        "New period date cannot be in the future."
                    )

                anchor_date = new_start
            else:
                anchor_date = first

            position = calculate_cycle_position(
                anchor_date,
                cycle_length,
                today
            )

            if logged:
                current_day = position.cycle_day
                current_description = (
                    "This is the first day of your period."
                    if current_day == 1
                    else f"{current_day} days into your recorded cycle."
                )
            else:
                current_day = (today - first).days + 1
                current_description = (
                    f"{current_day} days since menstruation began."
                )

            estimated_day = position.cycle_day

            if logged and position.cycle_day == 1:
                estimated_description = (
                    "Proposed first day of your cycle."
                )
            elif not logged and position.cycle_day == 1:
                estimated_description = (
                    "Proposed first day of your next cycle."
                )
            else:
                estimated_description = (
                    f"Estimated day {estimated_day} of your cycle."
                )

            self.current_day_label.config(
                text=str(current_day)
            )

            self.current_day_description.config(
                text=current_description
            )

            self.logged_status.config(
                text="Logged" if logged else "Not logged"
            )

            self.estimated_day_label.config(
                text=str(estimated_day)
            )

            self.estimated_description.config(
                text=estimated_description
            )

            self.estimated_date_label.config(
                text=(
                    "Proposed cycle start: "
                    f"{position.cycle_start.strftime('%B %d, %Y')}"
                )
            )

            # Identify the current estimated phase.
            phase = identify_phase(
                cycle_day=current_day,
                cycle_length=cycle_length,
                bleeding_duration=duration
            )

            self.phase_name_label.config(
                text=phase.phase_name
            )

            self.phase_stage_label.config(
                text=phase.phase_stage
            )

            self.phase_days_label.config(
                text=(
                    f"Estimated phase days: "
                    f"{phase.phase_start_day}?{phase.phase_end_day}\n"
                    f"Days remaining in this stage: {phase.days_remaining}"
                )
            )

            self.phase_estimate_label.config(
                text=(
                    f"Estimated ovulation day: "
                    f"Day {phase.estimated_ovulation_day}"
                )
            )

            self.info_label.config(
                text=(
                    f"Bleeding duration (last recorded): {duration} days\n"
                    f"Expected cycle length: {cycle_length} days\n"
                    f"Estimated next period: "
                    f"{position.next_estimated_period.strftime('%B %d, %Y')}"
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
