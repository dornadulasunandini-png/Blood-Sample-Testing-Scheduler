
import tkinter as tk
from tkinter import ttk, scrolledtext
from contextlib import redirect_stdout
from io import StringIO

from sample_data import display_samples
from brute_force import brute_force_scheduler
from divide_conquer import divide_conquer_scheduler

# Your current filename contains the spelling "dynamiv"
from dynamic_programming import dynamic_programming_scheduler

from greedy import greedy_scheduler
from comparision import compare_algorithms


# Create main window
root = tk.Tk()
root.title("Smart Blood Sample Testing Scheduler")
root.geometry("1100x700")
root.configure(bg="#eef3f8")


# Heading
heading = tk.Label(
    root,
    text="SMART BLOOD SAMPLE TESTING SCHEDULER",
    font=("Arial", 22, "bold"),
    bg="#17365d",
    fg="white",
    pady=20
)
heading.pack(fill="x")


subtitle = tk.Label(
    root,
    text="Hospital Laboratory Algorithm Management System",
    font=("Arial", 13),
    bg="#eef3f8",
    fg="#333333"
)
subtitle.pack(pady=10)


# Main frame
main_frame = tk.Frame(root, bg="#eef3f8")
main_frame.pack(fill="both", expand=True, padx=20, pady=10)


# Left button panel
button_frame = tk.Frame(
    main_frame,
    bg="white",
    padx=15,
    pady=15
)
button_frame.pack(side="left", fill="y", padx=(0, 15))


tk.Label(
    button_frame,
    text="ALGORITHM OPTIONS",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#17365d"
).pack(pady=15)


# Right output panel
output_frame = tk.Frame(
    main_frame,
    bg="white",
    padx=10,
    pady=10
)
output_frame.pack(side="right", fill="both", expand=True)


tk.Label(
    output_frame,
    text="SCHEDULER RESULTS",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#17365d"
).pack(pady=5)


output_box = scrolledtext.ScrolledText(
    output_frame,
    font=("Courier New", 11),
    wrap=tk.WORD,
    bg="#f8fafc",
    fg="#222222"
)
output_box.pack(fill="both", expand=True)


# Run selected algorithm
def run_algorithm(function):

    output_box.delete("1.0", tk.END)

    result = StringIO()

    try:
        with redirect_stdout(result):
            function()

        output_box.insert(tk.END, result.getvalue())

    except Exception as error:
        output_box.insert(
            tk.END,
            "ERROR:\n" + str(error)
        )


# Button style
style = ttk.Style()
style.configure(
    "Custom.TButton",
    font=("Arial", 11, "bold"),
    padding=10
)


# Algorithm buttons
buttons = [
    ("Display Blood Samples", display_samples),
    ("Brute Force Algorithm", brute_force_scheduler),
    ("Divide and Conquer", divide_conquer_scheduler),
    ("Dynamic Programming", dynamic_programming_scheduler),
    ("Greedy Algorithm", greedy_scheduler),
    ("Compare All Algorithms", compare_algorithms)
]


for button_text, function in buttons:

    ttk.Button(
        button_frame,
        text=button_text,
        style="Custom.TButton",
        command=lambda f=function: run_algorithm(f)
    ).pack(fill="x", pady=9)


# Clear button
ttk.Button(
    button_frame,
    text="Clear Results",
    style="Custom.TButton",
    command=lambda: output_box.delete("1.0", tk.END)
).pack(fill="x", pady=9)


# Exit button
ttk.Button(
    button_frame,
    text="Exit Application",
    style="Custom.TButton",
    command=root.destroy
).pack(fill="x", pady=9)


# Footer
tk.Label(
    root,
    text="Academic Project | Smart Blood Sample Testing Scheduler",
    font=("Arial", 10),
    bg="#17365d",
    fg="white",
    pady=12
).pack(fill="x")


# Start application
root.mainloop()
