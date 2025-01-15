import tkinter as tk
from tkinter import messagebox
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
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operation = operation_var.get()

        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 == 0:
                raise ZeroDivisionError("Division by zero is not allowed!")
            result = num1 / num2
        else:
            messagebox.showerror("Error", "Invalid operation selected!")
            return

        add_to_history(f"{num1} {operation} {num2}", result)
        result_label.config(text=f"Result: {result}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")
    except ZeroDivisionError as e:
        messagebox.showerror("Error", str(e))

def show_random_fact():
    """Show a random fact in a popup."""
    fact = random.choice(random_facts)
    messagebox.showinfo("Random Fact", fact)

# Expanded random facts list
random_facts = [
    "Did you know? Zero is the only number that can't be represented in Roman numerals.",
    "The number 7 is considered lucky in many cultures!",
    "Pi is an irrational number—it goes on forever without repeating.",
    "The word 'hundred' comes from the Old Norse word 'hundrath,' which actually means 120!",
    "A 'googol' is the number 1 followed by 100 zeros.",
    "In binary, the number 42 is written as 101010.",
    "Did you know? There are 86,400 seconds in a day!",
    "The Fibonacci sequence is often found in nature, like on sunflowers and your uncles baldspot cowlick!",
    "The number 4 is considered unlucky in China because it sounds like the word 'death.'",
    "Euler's number (e) is another famous irrational number.",
    "Multiplying any number by 9 and summing its digits results in 9 (e.g., 18 → 1+8=9).",
    "The first computer bug was an actual moth stuck in a Harvard Mark II computer in 1947."
]

# Initialize Tkinter GUI
root = tk.Tk()
root.title("Interactive Calculator")
root.geometry("500x500")

# Inputs
tk.Label(root, text="Enter first number:").pack()
entry_num1 = tk.Entry(root)
entry_num1.pack()

tk.Label(root, text="Enter second number:").pack()
entry_num2 = tk.Entry(root)
entry_num2.pack()

tk.Label(root, text="Select operation:").pack()
operation_var = tk.StringVar(value="+")
operations_menu = tk.OptionMenu(root, operation_var, "+", "-", "*", "/")
operations_menu.pack()

# Buttons
tk.Button(root, text="Calculate", command=calculate).pack()
tk.Button(root, text="Show Random Fact", command=show_random_fact).pack()

# Result Display
result_label = tk.Label(root, text="Result: ")
result_label.pack()

# History Display
tk.Label(root, text="Calculation History:").pack()
history_list = tk.Listbox(root, width=60, height=10)
history_list.pack()

# Load persistent history
for line in load_history():
    history_list.insert(tk.END, line.strip())

# Run GUI loop
root.mainloop()
