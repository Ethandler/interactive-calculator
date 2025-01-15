import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import datetime
import os

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

def calculate():
    """Perform the calculation based on user input."""
    try:
        numbers = [float(x) for x in simpledialog.askstring("Input", "Enter numbers separated by commas:").split(",")]
        operation = operation_var.get()

        if operation == "+":
            result = sum(numbers)
        elif operation == "-":
            result = numbers[0]
            for num in numbers[1:]:
                result -= num
        elif operation == "*":
            result = 1
            for num in numbers:
                result *= num
        elif operation == "/":
            result = numbers[0]
            for num in numbers[1:]:
                if num == 0:
                    raise ZeroDivisionError("Division by zero is not allowed!")
                result /= num
        else:
            messagebox.showerror("Error", "Invalid operation selected!")
            return

        add_to_history(f"{' '.join(map(str, numbers))} {operation}", result)
        result_label.config(text=f"Result: {result}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")
    except ZeroDivisionError as e:
        messagebox.showerror("Error", str(e))

def show_random_fact():
    """Show a random fact in the fact box."""
    fact = random.choice(random_facts)
    fact_label.config(text=fact)

def toggle_dark_mode():
    """Toggle between light and dark mode."""
    if root.cget("bg") == "#121212":
        root.config(bg="#f5f5f5")  # Softer light mode
        frame.config(bg="#eaeaea")
        fact_frame.config(bg="#ffffff")
        history_frame.config(bg="#f7f7f7")
        result_label.config(bg="#eaeaea", fg="black")
        fact_label.config(bg="#ffffff", fg="black")
        for widget in [frame, fact_frame, history_frame]:
            for child in widget.winfo_children():
                child.config(bg=widget.cget("bg"), fg="black")
        toggle_button.config(text="Dark Mode")
        calculate_button.config(bg="#4caf50", fg="white")  # Green for light mode
        random_fact_button.config(bg="#ff0000", fg="white")  # Red for light mode
    else:
        root.config(bg="#121212")
        frame.config(bg="#1e1e1e")
        fact_frame.config(bg="#1e1e1e")
        history_frame.config(bg="#1e1e1e")
        result_label.config(bg="#1e1e1e", fg="white")
        fact_label.config(bg="#1e1e1e", fg="white")
        for widget in [frame, fact_frame, history_frame]:
            for child in widget.winfo_children():
                child.config(bg=widget.cget("bg"), fg="white")
        toggle_button.config(text="Light Mode")
        calculate_button.config(bg="#ff00ff", fg="white")  # Neon pink for dark mode
        random_fact_button.config(bg="#8000ff", fg="white")  # Neon purple for dark mode

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

# Initialize Tkinter GUI
root = tk.Tk()
root.title("Interactive Calculator with Dark Mode")
root.geometry("600x600")
root.config(bg="#121212")

# Inputs
frame = tk.Frame(root, bg="#1e1e1e", bd=2, relief=tk.RIDGE, padx=10, pady=10)
frame.pack(pady=20)

tk.Label(frame, text="Interactive Calculator", font=("Helvetica", 16), bg="#1e1e1e", fg="white").pack()

operation_var = tk.StringVar(value="+")
tk.Label(frame, text="Select operation:", bg="#1e1e1e", fg="white").pack()
operations_menu = tk.OptionMenu(frame, operation_var, "+", "-", "*", "/")
operations_menu.pack()
operations_menu.config(bg="#1e1e1e", fg="white")

# Buttons
calculate_button = tk.Button(frame, text="Calculate", command=calculate, bg="#ff00ff", fg="white", padx=10, pady=5)
calculate_button.pack(pady=5)
random_fact_button = tk.Button(frame, text="Show Random Fact", command=show_random_fact, bg="#8000ff", fg="white", padx=10, pady=5)
random_fact_button.pack(pady=5)
toggle_button = tk.Button(frame, text="Light Mode", command=toggle_dark_mode, bg="#607d8b", fg="white", padx=10, pady=5)
toggle_button.pack(pady=5)

# Result Display
result_label = tk.Label(frame, text="Result: ", font=("Helvetica", 14), bg="#1e1e1e", fg="white")
result_label.pack()

# Fact Display
fact_frame = tk.Frame(root, bg="#1e1e1e", bd=2, relief=tk.GROOVE, padx=10, pady=10)
fact_frame.pack(pady=20)
tk.Label(fact_frame, text="Random Fact:", font=("Helvetica", 14), bg="#1e1e1e", fg="white").pack()
fact_label = tk.Label(fact_frame, text="", wraplength=500, bg="#1e1e1e", fg="white", font=("Helvetica", 12))
fact_label.pack()

# History Display
history_frame = tk.Frame(root, bg="#1e1e1e", bd=2, relief=tk.SUNKEN, padx=10, pady=10)
history_frame.pack(pady=20)
tk.Label(history_frame, text="Calculation History:", font=("Helvetica", 14), bg="#1e1e1e", fg="white").pack()
history_list = tk.Listbox(history_frame, width=60, height=10, bg="#1e1e1e", fg="white")
history_list.pack()

# Load persistent history
for line in load_history():
    history_list.insert(tk.END, line.strip())

# Run GUI loop
root.mainloop()
