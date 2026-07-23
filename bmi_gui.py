import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


DATA_FILE = "bmi_records.json"


def save_records(records):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def load_records():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def calculate_bmi(height, weight):
    height_m = height / 100
    bmi = weight / (height_m * height_m)
    return bmi


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "underweight"
    elif bmi < 24:
        return "normal weight"
    elif bmi < 28:
        return "overweight"
    else:
        return "obese"


def make_record(height, weight, bmi, result):
    person = {
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "result": result
    }

    return person


def format_number(number):
    return f"{number:g}"


def refresh_records():
    records = load_records()

    # Treeview 不会自动清空旧内容，所以刷新前先删除表格里的所有行。
    for item in records_tree.get_children():
        records_tree.delete(item)

    for index, person in enumerate(records, start=1):
        records_tree.insert(
            "",
            tk.END,
            values=(
                index,
                format_number(person["height"]),
                format_number(person["weight"]),
                round(person["bmi"], 2),
                person["result"]
            )
        )

    update_summary(records)


def update_summary(records):
    if len(records) == 0:
        average_bmi_label.config(text="Average BMI: No records")
        highest_bmi_label.config(text="Highest BMI record: No records")
        return

    average = sum(person["bmi"] for person in records) / len(records)

    bmi_values = []
    for person in records:
        bmi_values.append(person["bmi"])

    highest_bmi = max(bmi_values)

    highest_record_numbers = []
    for index, person in enumerate(records, start=1):
        if person["bmi"] == highest_bmi:
            highest_record_numbers.append(str(index))

    average_bmi_label.config(text=f"Average BMI: {round(average, 2)}")
    highest_bmi_label.config(
        text=(
            f"Highest BMI record: No. {', '.join(highest_record_numbers)} "
            f"(BMI: {round(highest_bmi, 2)})"
        )
    )


def calculate_and_save():
    height_text = height_entry.get().strip()
    weight_text = weight_entry.get().strip()

    try:
        height = float(height_text)
        weight = float(weight_text)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for height and weight.")
        return

    if not 50 <= height <= 250:
        messagebox.showerror("Input Error", "Please enter height between 50 and 250 cm.")
        return

    if not 10 <= weight <= 300:
        messagebox.showerror("Input Error", "Please enter weight between 10 and 300 kg.")
        return

    bmi = calculate_bmi(height, weight)
    result = get_bmi_category(bmi)

    result_label.config(
        text=(
            f"Height: {format_number(height)} cm\n"
            f"Weight: {format_number(weight)} kg\n"
            f"BMI: {round(bmi, 2)}\n"
            f"Category: {result}"
        )
    )

    records = load_records()
    records.append(make_record(height, weight, bmi, result))
    save_records(records)

    refresh_records()


def clear_inputs():
    height_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    result_label.config(text="Result will be shown here.")


window = tk.Tk()
window.title("BMI Calculator")
window.geometry("720x520")

main_frame = ttk.Frame(window, padding=12)
main_frame.pack(fill=tk.BOTH, expand=True)

input_frame = ttk.LabelFrame(main_frame, text="Input", padding=10)
input_frame.pack(fill=tk.X)

ttk.Label(input_frame, text="Height (cm):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
height_entry = ttk.Entry(input_frame, width=20)
height_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

ttk.Label(input_frame, text="Weight (kg):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
weight_entry = ttk.Entry(input_frame, width=20)
weight_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

button_frame = ttk.Frame(input_frame)
button_frame.grid(row=0, column=2, rowspan=2, sticky=tk.N, padx=20, pady=5)

calculate_button = ttk.Button(button_frame, text="Calculate and Save", command=calculate_and_save)
calculate_button.pack(fill=tk.X, pady=2)

clear_button = ttk.Button(button_frame, text="Clear Inputs", command=clear_inputs)
clear_button.pack(fill=tk.X, pady=2)

refresh_button = ttk.Button(button_frame, text="Refresh Records", command=refresh_records)
refresh_button.pack(fill=tk.X, pady=2)

result_frame = ttk.LabelFrame(main_frame, text="Result", padding=10)
result_frame.pack(fill=tk.X, pady=10)

result_label = ttk.Label(result_frame, text="Result will be shown here.")
result_label.pack(anchor=tk.W)

summary_frame = ttk.LabelFrame(main_frame, text="Summary", padding=10)
summary_frame.pack(fill=tk.X, pady=(0, 10))

average_bmi_label = ttk.Label(summary_frame, text="Average BMI: No records")
average_bmi_label.pack(anchor=tk.W)

highest_bmi_label = ttk.Label(summary_frame, text="Highest BMI record: No records")
highest_bmi_label.pack(anchor=tk.W)

records_frame = ttk.LabelFrame(main_frame, text="History Records", padding=10)
records_frame.pack(fill=tk.BOTH, expand=True)

columns = ("No.", "Height", "Weight", "BMI", "Category")
records_tree = ttk.Treeview(records_frame, columns=columns, show="headings")

# 给 Treeview 设置列名和列宽，让历史记录看起来像一个简单表格。
for column in columns:
    records_tree.heading(column, text=column)
    records_tree.column(column, width=100, anchor=tk.CENTER)

records_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=records_tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
records_tree.configure(yscrollcommand=scrollbar.set)

refresh_records()

window.mainloop()
