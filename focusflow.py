import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class FocusFlow:
    def __init__(self, root): 
        self.root = root
        self.root.title("FocusFlow - Productivity Timer")
        self.root.geometry("820x620")
        self.root.resizable(False, False)

        self.work_seconds = 25 * 60
        self.break_seconds = 5 * 60
        self.remaining = self.work_seconds
        self.running = False
        self.mode = "FOCUS"
        self.sessions = 0
        self.focus_minutes = 0
        self.tasks_done = 0
        self.history = []

        style = ttk.Style()
        style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"))
        style.configure("Timer.TLabel", font=("Segoe UI", 52, "bold"))
        style.configure("Card.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Action.TButton", font=("Segoe UI", 11, "bold"))

        header = ttk.Frame(root, padding=18)
        header.pack(fill="x")
        ttk.Label(header, text="FOCUSFLOW", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Productivity & Pomodoro Timer").pack(anchor="w")

        task_frame = ttk.LabelFrame(root, text="Current Task", padding=12)
        task_frame.pack(fill="x", padx=20, pady=5)

        self.task = tk.StringVar(value="")
        ttk.Entry(task_frame, textvariable=self.task, width=70).pack(side="left", padx=5)

        ttk.Button(task_frame, text="Mark Complete",
                   command=self.complete_task).pack(side="left", padx=5)

        timer = ttk.LabelFrame(root, text="Timer", padding=15)
        timer.pack(fill="x", padx=20, pady=10)

        self.mode_label = ttk.Label(timer, text="FOCUS")
        self.mode_label.pack()

        self.timer_label = ttk.Label(timer, text="25:00", style="Timer.TLabel")
        self.timer_label.pack(pady=5)

        buttons = ttk.Frame(timer)
        buttons.pack()

        self.start_btn = ttk.Button(
            buttons, text="START", style="Action.TButton",
            command=self.start_pause
        )
        self.start_btn.pack(side="left", padx=5)

        ttk.Button(
            buttons, text="RESET", style="Action.TButton",
            command=self.reset
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons, text="SKIP", style="Action.TButton",
            command=self.skip
        ).pack(side="left", padx=5)

        stats = ttk.Frame(root, padding=10)
        stats.pack(fill="x")

        self.sessions_var = tk.StringVar(value="0")
        self.focus_var = tk.StringVar(value="0 min")
        self.tasks_var = tk.StringVar(value="0")

        self.create_card(stats, "SESSIONS", self.sessions_var, 0)
        self.create_card(stats, "FOCUS TIME", self.focus_var, 1)
        self.create_card(stats, "TASKS DONE", self.tasks_var, 2)

        settings = ttk.LabelFrame(root, text="Timer Settings", padding=10)
        settings.pack(fill="x", padx=20, pady=5)

        ttk.Label(settings, text="Focus (minutes):").pack(side="left", padx=5)
        self.focus_entry = ttk.Entry(settings, width=7)
        self.focus_entry.insert(0, "25")
        self.focus_entry.pack(side="left")

        ttk.Label(settings, text="Break (minutes):").pack(side="left", padx=10)
        self.break_entry = ttk.Entry(settings, width=7)
        self.break_entry.insert(0, "5")
        self.break_entry.pack(side="left")

        ttk.Button(settings, text="Apply",
                   command=self.apply_settings).pack(side="left", padx=10)

        history_frame = ttk.LabelFrame(root, text="Session History", padding=8)
        history_frame.pack(fill="both", expand=True, padx=20, pady=8)

        columns = ("Time", "Task", "Type", "Duration")
        self.tree = ttk.Treeview(
            history_frame, columns=columns, show="headings", height=6
        )

        widths = {
            "Time": 120,
            "Task": 360,
            "Type": 100,
            "Duration": 100
        }

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.status = tk.StringVar(
            value="Ready. Enter a task and start focusing."
        )
        ttk.Label(
            root, textvariable=self.status, relief="sunken", anchor="w"
        ).pack(fill="x", side="bottom")

    def create_card(self, parent, title, variable, column):
        card = ttk.LabelFrame(parent, text=title, padding=12)
        card.grid(row=0, column=column, padx=8, sticky="ew")
        parent.columnconfigure(column, weight=1)
        ttk.Label(card, textvariable=variable,
                  style="Card.TLabel").pack()

    def start_pause(self):
        if self.running:
            self.running = False
            self.start_btn.config(text="RESUME")
            self.status.set("Timer paused.")
        else:
            self.running = True
            self.start_btn.config(text="PAUSE")
            self.status.set("Focus session running.")
            self.tick()

    def tick(self):
        if not self.running:
            return

        if self.remaining > 0:
            self.remaining -= 1
            self.update_timer()
            self.root.after(1000, self.tick)
        else:
            self.running = False
            self.start_btn.config(text="START")
            self.session_finished()

    def session_finished(self):
        duration = self.focus_minutes_setting()

        if self.mode == "FOCUS":
            self.sessions += 1
            self.focus_minutes += duration
            self.add_history("FOCUS", duration)

            self.mode = "BREAK"
            self.remaining = self.break_seconds
            self.status.set("Focus session complete. Time for a break!")
            messagebox.showinfo(
                "Focus Complete",
                "Great work! Your focus session is complete."
            )
        else:
            self.mode = "FOCUS"
            self.remaining = self.work_seconds
            self.status.set("Break complete. Ready for another focus session!")
            messagebox.showinfo(
                "Break Complete",
                "Break finished. Let's get back to work."
            )

        self.update_stats()
        self.update_timer()

    def focus_minutes_setting(self):
        try:
            return int(self.focus_entry.get())
        except ValueError:
            return 25

    def add_history(self, kind, duration):
        task = self.task.get().strip() or "General Productivity"
        row = (
            datetime.now().strftime("%H:%M"),
            task,
            kind,
            f"{duration} min"
        )
        self.history.append(row)
        self.tree.insert("", "end", values=row)

    def complete_task(self):
        task = self.task.get().strip()

        if not task:
            messagebox.showwarning(
                "Task Required",
                "Enter a task before marking it complete."
            )
            return

        self.tasks_done += 1
        self.tasks_var.set(str(self.tasks_done))
        self.status.set(f"Task completed: {task}")
        self.task.set("")

    def apply_settings(self):
        try:
            focus = int(self.focus_entry.get())
            break_time = int(self.break_entry.get())

            if focus <= 0 or break_time <= 0:
                raise ValueError

            if self.running:
                messagebox.showwarning(
                    "Timer Running",
                    "Pause the timer before changing settings."
                )
                return

            self.work_seconds = focus * 60
            self.break_seconds = break_time * 60
            self.mode = "FOCUS"
            self.remaining = self.work_seconds
            self.update_timer()
            self.status.set("Timer settings updated.")

        except ValueError:
            messagebox.showerror(
                "Invalid Settings",
                "Enter positive whole numbers for the timer."
            )

    def reset(self):
        self.running = False
        self.start_btn.config(text="START")

        if self.mode == "FOCUS":
            self.remaining = self.work_seconds
        else:
            self.remaining = self.break_seconds

        self.update_timer()
        self.status.set("Timer reset.")

    def skip(self):
        self.running = False
        self.start_btn.config(text="START")

        if self.mode == "FOCUS":
            self.mode = "BREAK"
            self.remaining = self.break_seconds
        else:
            self.mode = "FOCUS"
            self.remaining = self.work_seconds

        self.update_timer()
        self.status.set(f"Switched to {self.mode.lower()} mode.")

    def update_timer(self):
        minutes = self.remaining // 60
        seconds = self.remaining % 60

        self.timer_label.config(
            text=f"{minutes:02d}:{seconds:02d}"
        )
        self.mode_label.config(text=self.mode)

    def update_stats(self):
        self.sessions_var.set(str(self.sessions))
        self.focus_var.set(f"{self.focus_minutes} min")
        self.tasks_var.set(str(self.tasks_done))


if __name__ == "__main__":
    root = tk.Tk()
    app = FocusFlow(root)
    root.mainloop()
