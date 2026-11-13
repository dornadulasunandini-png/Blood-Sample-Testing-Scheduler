
import tkinter as tk
from tkinter import messagebox
from time import perf_counter
from contextlib import redirect_stdout
from io import StringIO

from brute_force import brute_force_scheduler
from divide_conquer import divide_conquer_scheduler
from dynamic_programming import dynamic_programming_scheduler
from greedy import greedy_scheduler


# Algorithms
algorithms = [
    ("Brute Force", brute_force_scheduler),
    ("Divide and Conquer", divide_conquer_scheduler),
    ("Dynamic Programming", dynamic_programming_scheduler),
    ("Greedy", greedy_scheduler)
]


# Measure execution time
def measure_time(function):

    output = StringIO()

    start = perf_counter()

    with redirect_stdout(output):
        function()

    end = perf_counter()

    return (end - start) * 1000


# Display chart
def run_comparison():

    run_button.config(state="disabled", text="Calculating...")
    status_label.config(text="Please wait... Running algorithms")
    root.update_idletasks()

    try:
        results = []

        for name, function in algorithms:
            elapsed = measure_time(function)
            results.append((name, elapsed))

        chart.delete("all")

        chart.create_text(
            420, 25,
            text="ALGORITHM EXECUTION TIME COMPARISON",
            font=("Arial", 16, "bold"),
            fill="#17365d"
        )

        max_time = max(value for name, value in results)

        if max_time <= 0:
            max_time = 1

        for i, (name, elapsed) in enumerate(results):

            y = 85 + i * 85

            bar_width = max(2, (elapsed / max_time) * 450)

            chart.create_text(
                145, y + 18,
                text=name,
                font=("Arial", 11, "bold"),
                anchor="e",
                fill="#222222"
            )

            chart.create_rectangle(
                165, y,
                165 + bar_width, y + 38,
                fill="#2878b5",
                outline=""
            )

            chart.create_text(
                175 + bar_width,
                y + 19,
                text=f"{elapsed:.4f} ms",
                anchor="w",
                font=("Arial", 10),
                fill="#222222"
            )

        chart.create_text(
            420, 450,
            text="Lower execution time means faster execution",
            font=("Arial", 11, "italic"),
            fill="#555555"
        )

        status_label.config(
            text="Comparison completed successfully!"
        )

    except Exception as error:
        messagebox.showerror("Error", str(error))
        status_label.config(text="Comparison failed. Check the error.")

    finally:
        run_button.config(
            state="normal",
            text="RUN PERFORMANCE COMPARISON"
        )


# Main window
root = tk.Tk()
root.title("Smart Blood Sample Scheduler - Performance Analysis")
root.geometry("950x650")
root.configure(bg="#eef3f8")
root.minsize(800, 600)


# Heading
tk.Label(
    root,
    text="ALGORITHM PERFORMANCE ANALYSIS",
    font=("Arial", 20, "bold"),
    bg="#17365d",
    fg="white",
    pady=18
).pack(fill="x")


# Description
tk.Label(
    root,
    text="Compare the execution time of four algorithms",
    font=("Arial", 12),
    bg="#eef3f8"
).pack(pady=8)


# Button - placed BEFORE chart
run_button = tk.Button(
    root,
    text="RUN PERFORMANCE COMPARISON",
    font=("Arial", 12, "bold"),
    bg="#17365d",
    fg="white",
    activebackground="#2878b5",
    activeforeground="white",
    padx=20,
    pady=10,
    command=run_comparison
)

run_button.pack(pady=8)


# Status message
status_label = tk.Label(
    root,
    text="Click the button to compare algorithms",
    font=("Arial", 10),
    bg="#eef3f8",
    fg="#17365d"
)
status_label.pack(pady=5)


# Chart area
chart = tk.Canvas(
    root,
    width=900,
    height=490,
    bg="white",
    highlightthickness=0
)

chart.pack(fill="both", expand=True, padx=20, pady=10)


# Footer
tk.Label(
    root,
    text="Smart Blood Sample Testing Scheduler | Academic Project",
    font=("Arial", 10),
    bg="#17365d",
    fg="white",
    pady=8
).pack(fill="x")


root.mainloop()
