import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import os
import math
from fractions import Fraction
import re

# Expanded random facts list
random_facts = [
    "Did you know? Zero is the only number that can't be represented in Roman numerals.",
    "The number 7 is considered lucky in many cultures!",
    "Pi is an irrational number—it goes on forever without repeating.",
    "The word 'hundred' comes from the Old Norse word 'hundrath,' which actually means 120!",
    "A 'googol' is the number 1 followed by 100 zeros.",
    "In binary, the number 42 is written as 101010.",
    "Did you know? There are 86,400 seconds in a day!",
    "The Fibonacci sequence is often found in nature, like pinecones and sunflowers.",
    "The number 4 is considered unlucky in China because it sounds like the word 'death.'",
    "Euler's number (e) is another famous irrational number.",
    "Multiplying any number by 9 and summing its digits results in 9 (e.g., 18 → 1+8=9).",
    "The first computer bug was an actual moth stuck in a Harvard Mark II computer in 1947."
]

# File to store persistent history
HISTORY_FILE = "calc_history.txt"

def load_history():
    """Load history from file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as file:
        return file.readlines()

def save_history(entry):
    """Save a history entry to the file."""
    with open(HISTORY_FILE, "a") as file:
        file.write(entry + "\n")

def add_to_history(expression, result):
    """Add a new calculation to the history with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} | {expression} = {result}"
    history_list.insert(tk.END, entry)
    save_history(entry)

def parse_expression(expression):
    """Parse and evaluate the expression safely."""
    try:
        # Convert standalone fractions
        expression = re.sub(r'\b(\d+)/(\d+)\b', r'Fraction(\1, \2)', expression)
        expression = expression.replace("sqrt", "math.sqrt").replace("SQ", "math.sqrt")
        result = eval(expression, {"math": math, "Fraction": Fraction})
        return result
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

def calculate():
    """Perform the calculation based on user input."""
    try:
        expression = input_entry.get()
        if not expression:
            return
        result = parse_expression(expression)
        result_label.config(text=f"Result: {result}")
        add_to_history(expression, result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_random_fact():
    """Show a random fact in the fact box."""
    fact = random.choice(random_facts)
    fact_label.config(text=fact)

def close_app():
    """Close the application with a confirmation message."""
    if messagebox.askokcancel("Quit", "Nooo! Don't kill me! JKJK have a nice day! ;)"):
        root.destroy()

# Initialize Tkinter GUI
root = tk.Tk()
root.title("Interactive Calculator with Dark Mode")
root.geometry("800x700")  # Slightly bigger default size
root.config(bg="#121212")

# Tab Control Style
style = ttk.Style()
try:
    style.theme_create("darkmode", parent="clam", settings={
        "TNotebook": {"configure": {"background": "#121212", "tabmargins": [2, 5, 2, 0]}},
        "TNotebook.Tab": {
            "configure": {"background": "#1e1e1e", "foreground": "white"}
        }
    })
    style.theme_use("darkmode")
except tk.TclError as e:
    print(f"Theme creation failed: {e}")
    style.theme_use("clam")

# Tab Control
tab_control = ttk.Notebook(root)
main_tab = ttk.Frame(tab_control, style="TNotebook")
history_tab = ttk.Frame(tab_control, style="TNotebook")

# Add Tabs
tab_control.add(main_tab, text="Calculator")
tab_control.add(history_tab, text="History")
tab_control.pack(expand=1, fill="both")

# Main Tab (Calculator)
frame = tk.Frame(main_tab, bg="#1e1e1e", bd=2, relief=tk.RIDGE, padx=10, pady=10)
frame.pack(pady=20)

tk.Label(frame, text="Interactive Calculator", font=("Helvetica", 16), bg="#1e1e1e", fg="white").pack()

# Input Frame
input_frame = tk.Frame(main_tab, bg="#1e1e1e")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Enter Calculation (e.g., SQ(16) for sqrt):", font=("Helvetica", 12), bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
input_entry = tk.Entry(input_frame, width=40, bg="#1e1e1e", fg="white")
input_entry.pack(side=tk.LEFT, padx=5)
calculate_button = tk.Button(input_frame, text="Calculate", command=calculate, bg="#ff00ff", fg="white")
calculate_button.pack(side=tk.LEFT)

# Random Fact Button
random_fact_button = tk.Button(frame, text="Show Random Fact", command=show_random_fact, bg="#8000ff", fg="white", padx=10, pady=5)
random_fact_button.pack(pady=5)

close_button = tk.Button(frame, text="Close Me", command=close_app, bg="#607d8b", fg="white", padx=10, pady=5)
close_button.pack(pady=5)

# Result Display
result_label = tk.Label(frame, text="Result: ", font=("Helvetica", 14), bg="#1e1e1e", fg="white")
result_label.pack()

# Fact Display
fact_frame = tk.Frame(main_tab, bg="#1e1e1e", bd=2, relief=tk.GROOVE, padx=10, pady=10)
fact_frame.pack(pady=20)
tk.Label(fact_frame, text="Random Fact:", font=("Helvetica", 14), bg="#1e1e1e", fg="white").pack()
fact_label = tk.Label(fact_frame, text="", wraplength=500, bg="#1e1e1e", fg="white", font=("Helvetica", 12))
fact_label.pack()

# History Tab
history_frame = tk.Frame(history_tab, bg="#1e1e1e", bd=2, relief=tk.SUNKEN, padx=10, pady=10)
history_frame.pack(pady=20, fill="both", expand=True)
tk.Label(history_frame, text="Calculation History:", font=("Helvetica", 14), bg="#1e1e1e", fg="white").pack()
history_list = tk.Listbox(history_frame, width=80, height=20, bg="#1e1e1e", fg="white")
history_list.pack(fill="both", expand=True)

# Load persistent history
for line in load_history():
    history_list.insert(tk.END, line.strip())

# Run GUI loop
tk.mainloop()
