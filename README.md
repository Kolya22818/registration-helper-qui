# 🛰️ КЧП Регистратор (копипастер)

**Программа для ускорения ручного заполнения анкет, форм и онлайн-систем.**  
Позволяет копировать данные из локального окна и вставлять их в любое внешнее приложение простыми действиями мыши. Подходит для работы с государственными порталами, системами приёма заявлений, HR-формами и др.

---

## 📦 Возможности

- 🔘 Копирование данных из своего окна по клику мыши
- 🖱️ Вставка данных по **правому клику** вне окна программы
- 🖱️ **Двойной клик вне окна** → вставка + переход к следующему полю
- 👤 Переключение между пользователями кнопками "← Назад" и "Вперёд →"
- 🔁 Автоматический переход по полям (`advance`)
- ⌨ Глобальные горячие клавиши:
  - `Ctrl + 1` — запуск автозаполнения
  - `Ctrl + 2` — остановка автозаполнения

---

## 🔧 Установка

### 1. Установите Python 3.10+

Скачайте с [https://www.python.org](https://www.python.org) и установите.  
⚠ Не забудьте поставить галочку: **"Add Python to PATH"** при установке.

---

### 2. Установите зависимости

Откройте терминал и выполните по очереди:

```bash
pip install pandas
pip install pyperclip
pip install --no-cache-dir pyautogui
pip install pynput
pip install keyboard
pip install pywin32
🔒 --no-cache-dir при установке pyautogui снижает шанс установки повреждённой версии.

3. Запуск программы

python registration-helper-gui.py

🗂 Формат файла users.json
Файл users.json должен находиться в одной папке с программой и содержать массив пользователей в формате:

[
  {
    "INPOL": "0123456",
    "MOS": "01234567",
    "Имя": "artem",
    "Фам": "Szachilow",
    "Др": "11.03.1999",
    "Паспорт": "AA01223456",
    "Граж": "Tadzikistan",
    "Тел": "+48111111111",
    "Email": "artem@example.com"
  }
]

🖱 Как пользоваться
Клик по полю — копирует значение в буфер обмена.

ПКМ в другом приложении — вставляет скопированное.

Двойной клик вне окна — вставляет и переходит к следующему полю.

Переключение пользователей — вручную с помощью кнопок внизу.

Горячие клавиши:

Ctrl+1 — запуск

Ctrl+2 — остановка

🔘 Интерфейс
Кнопка	Назначение
▶ Запустить	Включить режим автозаполнения
⏹ Стоп	Остановить режим автозаполнения
← Назад	Предыдущий пользователь
→ Вперёд	Следующий пользователь
⚠️ Важно
Программа работает только на Windows

Всегда остаётся поверх других окон (topmost)

Использует ctrl + v для вставки (работает в браузерах, Excel и др.)

Убедитесь, что файл users.json валиден

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
📁 Описание проекта: "Registration Helper GUI"
Это локальное приложение на Python, которое:

читает данные из файла users.json (список людей),

показывает их в окне,

позволяет вставлять данные в браузерные формы по кнопке Вставить,

помогает быстро регистрировать людей на ограниченное время (например, в Ужонде).

🔧 Что нужно для запуска
1. Установить Python (если не установлен)
Скачай с официального сайта:
🔗 https://www.python.org/downloads/
✅ При установке поставь галочку "Add Python to PATH"!

2. Клонировать репозиторий с GitHub
Если установлен Git:

git clone https://github.com/Kolya22818/registration-helper-qui.git
cd registration-helper-qui
Или просто скачай ZIP-архив с GitHub и распакуй.

3. Установить зависимости
Открой терминал (или PowerShell в папке проекта) и выполни:

pip install pandas pyperclip pyautogui
📂 Структура проекта

registration-helper-qui/
├── main.py           ← главный скрипт (может называться registration-helper-gui.py)
├── users.json        ← файл с данными пользователей
├── README.md         ← описание проекта
✍️ Формат файла users.json
Это обычный текстовый файл в формате JSON со списком людей:

[
  {
    "INPOL": "00012345",
    "MOS": "00056789",
    "Имя": "Иван",
    "Фамилия": "Петров",
    "Дата рождения": "01.01.1990",
    "Номер паспорта": "AA1234567",
    "Гражданство": "Украина",
    "Телефон": "+48123456789",
    "Email": "ivan@example.com"
  }
]
Можешь добавить несколько людей — по одному объекту в массиве [...].

🚀 Как пользоваться
1. Запусти программу:

python main.py
(или python registration-helper-gui.py, если у тебя так называется)

2. В окне ты увидишь поля с данными одного пользователя.
Кнопки "Вставить" вставляют данные в активное поле браузера с помощью Ctrl+V.

3. Перед нажатием «Вставить»:
вручную кликни мышкой в нужное поле формы в браузере,

затем нажми «Вставить» в приложении.

4. Навигация:
← Назад — предыдущий человек

→ Следующий — следующий человек

Индикатор снизу показывает, какой человек сейчас отображается.

🧠 Что важно знать
Окно программы всегда поверх — удобно вставлять, не переключаясь.

Ты сам решаешь, куда вставлять — программа не кликает мышкой, только вставляет.

Можно легко редактировать users.json в любом редакторе (например, Notepad++ или VS Code).

🔒 Безопасность
Никакие данные никуда не отправляются.

Всё работает локально на твоём компьютере.

❓ Частые вопросы
Q: Почему вставка не работает?
A: Убедись, что ты:

кликнул в нужное поле в браузере,

затем нажал кнопку «Вставить»,

не используешь антивирус или защиту, блокирующую pyautogui.

Q: Как сделать .exe файл?
A: Скажи, и я соберу инструкцию под PyInstaller.

