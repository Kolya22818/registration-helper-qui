import tkinter as tk
import pandas as pd
import pyperclip
import pyautogui
import json
import threading
import time
from pynput import mouse
from tkinter import messagebox

# Попытка загрузить данные
try:
    with open("users.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
except Exception as e:
    messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить users.json:\n{e}")
    exit()

fields_order = ["INPOL", "MOS", "Имя", "Фамилия", "Дата рождения", "Номер паспорта", "Гражданство", "Телефон", "Email"]
current_person = 0
current_field = 0
auto_mode = False

# GUI
root = tk.Tk()
root.title("КЧП Регистратор")
root.geometry("340x360")
root.wm_attributes("-topmost", 1)
root.wm_attributes("-alpha", 0.9)

field_vars = {}
entry_widgets = {}

def update_display():
    for key in fields_order:
        entry_widgets[key].config(bg="white")
    if current_person < len(df):
        person = df.iloc[current_person]
        for key in fields_order:
            value = str(person.get(key, ""))
            field_vars[key].set(value)
        current_field_name = fields_order[current_field]
        current_value = str(person.get(current_field_name, ""))
        pyperclip.copy(current_value)
        entry_widgets[current_field_name].config(bg="lightgreen")
        print(f"[Скопировано] {current_field_name}: {current_value}")
    else:
        status_label.config(text="✅ Все пользователи обработаны.")
        auto_mode_off()

def advance():
    global current_field, current_person
    current_field += 1
    if current_field >= len(fields_order):
        current_field = 0
        current_person += 1
        if current_person >= len(df):
            print("✅ Все пользователи обработаны.")
            return
    update_display()

def start_auto_mode():
    global auto_mode
    auto_mode = True
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    status_label.config(text="🔛 Автовставка активна")
    update_display()

def auto_mode_off():
    global auto_mode
    auto_mode = False
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    status_label.config(text="⏸ Автовставка остановлена")

# Обработка клика мыши
def on_click(x, y, button, pressed):
    if pressed and auto_mode and current_person < len(df):
        try:
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "v")
            threading.Timer(0.2, advance).start()
        except Exception as e:
            print(f"[Ошибка вставки] {e}")

# Слушатель мыши в отдельном потоке
def start_mouse_listener():
    listener = mouse.Listener(on_click=on_click)
    listener.daemon = True
    listener.start()

threading.Thread(target=start_mouse_listener, daemon=True).start()

# Интерфейс
for i, key in enumerate(fields_order):
    tk.Label(root, text=key).grid(row=i, column=0, sticky="w")
    var = tk.StringVar()
    entry = tk.Entry(root, textvariable=var, width=25)
    entry.grid(row=i, column=1)
    field_vars[key] = var
    entry_widgets[key] = entry

start_button = tk.Button(root, text="▶ Запустить", command=start_auto_mode, bg="lightgreen", font=("Arial", 10, "bold"))
start_button.grid(row=len(fields_order), column=0, pady=10)

stop_button = tk.Button(root, text="⏹ Стоп", command=auto_mode_off, bg="tomato", font=("Arial", 10, "bold"), state="disabled")
stop_button.grid(row=len(fields_order), column=1, pady=10)

status_label = tk.Label(root, text="⏸ Ожидает запуска", font=("Arial", 9, "italic"))
status_label.grid(row=len(fields_order)+1, column=0, columnspan=2)

root.mainloop()
