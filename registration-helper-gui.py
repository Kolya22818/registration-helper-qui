import tkinter as tk
import pandas as pd
import pyperclip
import pyautogui
import json
import threading
import time
import sys
from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
import win32gui
from tkinter import messagebox

# === Глобальные переменные ===
fields_order = [
    "INPOL", "MOS", "Имя", "Фам", "Др",
    "Паспорт", "Граж", "Тел", "Email"
]
current_person = 0
current_field = 0
auto_mode = False
program_hwnd = None
last_click_time = 0
click_threshold = 0.3

field_vars = {}
entry_widgets = {}
pressed_keys = set()

# === Загрузка данных ===
def load_data():
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        if df.empty:
            messagebox.showerror("Ошибка", "Файл users.json пуст.")
            return None
        return df
    except Exception as e:
        messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить users.json:\n{e}")
        return None

df = load_data()
if df is None:
    sys.exit()

# === GUI ===
root = tk.Tk()
root.title("КЧПР")
root.geometry("250x300")
root.wm_attributes("-topmost", 1)
root.wm_attributes("-alpha", 0.90)

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

for i, key in enumerate(fields_order):
    tk.Label(frame, text=key).grid(row=i, column=0, sticky="w")
    var = tk.StringVar()
    entry = tk.Entry(frame, textvariable=var, width=25)
    entry.grid(row=i, column=1)
    field_vars[key] = var
    entry_widgets[key] = entry

status_label = tk.Label(frame, text="⏸ Ожидает запуска", font=("Arial", 9, "italic"))
status_label.grid(row=len(fields_order), column=0, columnspan=2, pady=(10, 0))

# === Функции логики ===
def update_display():
    for key in fields_order:
        entry_widgets[key].config(bg="white")
    if current_person < len(df):
        person = df.iloc[current_person]
        for key in fields_order:
            field_vars[key].set(str(person.get(key, "")))
        current_key = fields_order[current_field]
        value = str(person.get(current_key, ""))
        try:
            pyperclip.copy(value)
        except Exception as e:
            print(f"[Ошибка буфера] {e}")
        entry_widgets[current_key].config(bg="lightgreen")
        status_label.config(text=f"👤 Пользователь {current_person + 1} из {len(df)}")
        print(f"[Скопировано] {current_key}: {value}")
    else:
        status_label.config(text="✅ Все пользователи обработаны.")
        auto_mode_off()

def advance():
    global current_field, current_person
    if not auto_mode:
        return
    current_field += 1
    if current_field >= len(fields_order):
        current_field = 0
        current_person += 1
        if current_person >= len(df):
            print("✅ Все пользователи обработаны.")
            return
    update_display()

def start_auto_mode():
    global auto_mode, program_hwnd
    auto_mode = True
    program_hwnd = win32gui.GetForegroundWindow()
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

def prev_person():
    global current_person, current_field
    if current_person > 0:
        current_person -= 1
        current_field = 0
        update_display()

def next_person():
    global current_person, current_field
    if current_person < len(df) - 1:
        current_person += 1
        current_field = 0
        update_display()

def prev_person():
    global current_index
    if current_index > 0:
        current_index -= 1
        update_fields()
    else:
        now = time.time()
        if now - last_click_time <= click_threshold and auto_mode:
            try:
                hwnd = win32gui.GetForegroundWindow()
                if hwnd != program_hwnd:
                    pyautogui.hotkey("ctrl", "v")
                    print("✅ Вставка по двойному щелчку")
                    threading.Timer(0.2, advance).start()
            except Exception as e:
                print(f"[Ошибка вставки] {e}")
        elif button == Button.right and auto_mode:
            try:
                pyautogui.hotkey("ctrl", "v")
                print("🔁 Вставка по правому клику")
            except Exception as e:
                print(f"[Ошибка вставки ПКМ] {e}")
        last_click_time = time.time()

# === Обработка клавиатуры ===
def on_key_press(key):
    try:
        pressed_keys.add(key)
        if any(k in pressed_keys for k in [Key.ctrl, Key.ctrl_l, Key.ctrl_r]):
            if hasattr(key, 'char'):
                if key.char == '1':
                    print("▶ Горячая клавиша Ctrl+1")
                    start_auto_mode()
                elif key.char == '2':
                    print("⏹ Горячая клавиша Ctrl+2")
                    auto_mode_off()
    except Exception as e:
        print(e)

def on_key_release(key):
    pressed_keys.discard(key)

# === Слушатели ===
def start_mouse_listener():
    listener = mouse.Listener(on_click=on_click)
    listener.daemon = True
    listener.start()

def start_keyboard_listener():
    listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    listener.daemon = True
    listener.start()

# === Кнопки ===
start_button = tk.Button(frame, text="▶ Запустить", command=start_auto_mode, bg="lightgreen", font=("Arial", 10, "bold"))
start_button.grid(row=len(fields_order)+1, column=0, pady=5)

stop_button = tk.Button(frame, text="⏹ Стоп", command=auto_mode_off, bg="tomato", font=("Arial", 10, "bold"), state="disabled")
stop_button.grid(row=len(fields_order)+1, column=1, pady=5)

prev_button = tk.Button(frame, text="← Назад", command=prev_person, font=("Arial", 9))
prev_button.grid(row=len(fields_order)+2, column=0, pady=5)

next_button = tk.Button(frame, text="Вперёд →", command=next_person, font=("Arial", 9))
next_button.grid(row=len(fields_order)+2, column=1, pady=5)

# === Запуск ===
threading.Thread(target=start_mouse_listener, daemon=True).start()
threading.Thread(target=start_keyboard_listener, daemon=True).start()

root.mainloop()