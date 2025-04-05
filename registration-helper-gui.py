import tkinter as tk
from tkinter import messagebox
import pandas as pd
import pyperclip
import pyautogui
import time
from functools import partial
import json

# Загрузка данных из локального JSON-файла
json_file_path = "users.json"
try:
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
except Exception as e:
    messagebox.showerror("Ошибка", f"Не удалось загрузить JSON-файл: {e}")
    exit()

current_index = 0

def update_fields():
    if 0 <= current_index < len(df):
        person = df.iloc[current_index]
        inpol_var.set(person['INPOL'])
        mos_var.set(person['MOS'])
        name_var.set(person['Имя'])
        surname_var.set(person['Фамилия'])
        birth_var.set(person['Дата рождения'])
        passport_var.set(person['Номер паспорта'])
        citizen_var.set(person['Гражданство'])
        phone_var.set(person['Телефон'])
        email_var.set(person['Email'])
        position_label_var.set(f"Пользователь {current_index + 1} из {len(df)}")

def paste_field(var):
    value = var.get()
    pyperclip.copy(value)
    time.sleep(1.00)
    pyautogui.hotkey("ctrl", "v")

def next_person():
    global current_index
    if current_index < len(df) - 1:
        current_index += 1
        update_fields()

def prev_person():
    global current_index
    if current_index > 0:
        current_index -= 1
        update_fields()
    else:
        messagebox.showinfo("Начало", "Вы на первом пользователе.")

# GUI
root = tk.Tk()
root.title("Регистратор")
root.geometry("520x550")
root.attributes('-topmost', True)

inpol_var = tk.StringVar()
mos_var = tk.StringVar()
name_var = tk.StringVar()
surname_var = tk.StringVar()
birth_var = tk.StringVar()
passport_var = tk.StringVar()
citizen_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
position_label_var = tk.StringVar()

fields = [
    ("Kod z systemu INPOL", inpol_var),
    ("Kod z portalu MOS", mos_var),
    ("Имя", name_var),
    ("Фамилия", surname_var),
    ("Дата рождения", birth_var),
    ("Паспорт", passport_var),
    ("Гражданство", citizen_var),
    ("Телефон", phone_var),
    ("Email", email_var)
]

for i, (label, var) in enumerate(fields):
    tk.Label(root, text=label).grid(row=i, column=0, sticky="w")
    tk.Entry(root, textvariable=var, width=30).grid(row=i, column=1)
    tk.Button(root, text="Вставить", command=partial(paste_field, var)).grid(row=i, column=2)

# Индикатор текущей позиции
position_label = tk.Label(root, textvariable=position_label_var, font=("Arial", 10, "bold"))
position_label.grid(row=len(fields), column=0, columnspan=3, pady=(5, 0))

# Кнопки управления
button_frame = tk.Frame(root)
button_frame.grid(row=len(fields)+1, column=0, columnspan=3, pady=10)

tk.Button(button_frame, text="← Назад", command=prev_person, bg="lightblue").pack(side="left", padx=5)
tk.Button(button_frame, text="Следующий →", command=next_person, bg="lightgreen").pack(side="right", padx=5)

update_fields()
root.mainloop()
