import tkinter as tk
from tkinter import messagebox
import json
import os

# -------------------------
# Habit Class
# -------------------------
class Habit:
    def __init__(self, name, category, frequency, last_done=None):
        self.name = name
        self.category = category
        self.frequency = frequency
        self.last_done = last_done

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "frequency": self.frequency,
            "last_done": self.last_done
        }

# -------------------------
# Data Manager (Load/Save)
# -------------------------
DATA_FILE = "storage.json"

def load_habits():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_habits(habits):
    with open(DATA_FILE, "w") as file:
        json.dump(habits, file, indent=4)

# -------------------------
# Controller (Logic)
# -------------------------
class HabitController:
    def __init__(self):
        self.habits = load_habits()

    def add_habit(self, habit_dict):
        self.habits.append(habit_dict)
        save_habits(self.habits)

    def delete_habit(self, index):
        if 0 <= index < len(self.habits):
            del self.habits[index]
            save_habits(self.habits)

    def get_all(self):
        return self.habits

# -------------------------
# GUI Application (Tkinter)
# -------------------------
controller = HabitController()

# 🎨 COLORS & FONTS
BG_COLOR = "#2C2F33"
INPUT_BG = "#23272A"
BTN_COLOR = "#7289DA"
BTN_HOVER = "#5b6eae"
TEXT_COLOR = "#FFFFFF"
FONT = ("Segoe UI", 10)
HEADER_FONT = ("Segoe UI", 14, "bold")

# Create GUI window
root = tk.Tk()
root.title("🧠 CodeWhiz - Coding Habit Monitor")
root.geometry("600x500")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# ---------- Functions ----------

def add_habit():
    name = name_entry.get()
    category = category_entry.get()
    frequency = frequency_entry.get()

    if not name.strip():
        messagebox.showerror("Input Error", "Habit name is required!")
        return

    habit = Habit(name, category, frequency)
    controller.add_habit(habit.to_dict())
    update_list()
    clear_fields()

def delete_selected():
    try:
        selected_index = habit_list.curselection()[0]
        controller.delete_habit(selected_index)
        update_list()
    except IndexError:
        messagebox.showwarning("No Selection", "Please select a habit to delete.")

def update_list():
    habit_list.delete(0, tk.END)
    for habit in controller.get_all():
        habit_list.insert(tk.END, f"{habit['name']} | {habit['category']} | {habit['frequency']}")

def clear_fields():
    name_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    frequency_entry.delete(0, tk.END)

# ---------- Widgets ----------

# Header Label
tk.Label(root, text="📋 Coding Habit Tracker", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

# Form Frame
form_frame = tk.Frame(root, bg=BG_COLOR)
form_frame.pack(pady=10)

def create_label(text, row):
    tk.Label(form_frame, text=text, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).grid(row=row, column=0, padx=10, pady=8, sticky="e")

def create_entry(row):
    entry = tk.Entry(form_frame, width=30, bg=INPUT_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR)
    entry.grid(row=row, column=1, padx=10, pady=8)
    return entry

create_label("Habit Name:", 0)
name_entry = create_entry(0)

create_label("Category:", 1)
category_entry = create_entry(1)

create_label("Frequency:", 2)
frequency_entry = create_entry(2)

# Buttons Frame
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

add_btn = tk.Button(btn_frame, text="➕ Add Habit", bg=BTN_COLOR, fg="white", font=FONT, width=15, command=add_habit)
add_btn.grid(row=0, column=0, padx=10)

delete_btn = tk.Button(btn_frame, text="🗑 Delete Selected", bg="#E74C3C", fg="white", font=FONT, width=15, command=delete_selected)
delete_btn.grid(row=0, column=1, padx=10)

# Listbox Frame
list_frame = tk.Frame(root, bg=BG_COLOR)
list_frame.pack(pady=20)

habit_list = tk.Listbox(
    list_frame,
    width=65,
    height=10,
    bg=INPUT_BG,
    fg=TEXT_COLOR,
    font=("Courier New", 10),
    selectbackground="#5865F2",
    selectforeground="white",
    borderwidth=0,
    highlightthickness=1,
    relief="flat"
)
habit_list.pack()

# Initialize habit list
update_list()

# Run the GUI loop
root.mainloop()
