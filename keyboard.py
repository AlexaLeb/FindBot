from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import calendar
from datetime import datetime


def keyb():
    kb = [
        [
            KeyboardButton(text='Я потерял кое-что'),
            KeyboardButton(text='Я нашел кое-что')
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def approve_kb():
    kb = [
        [
            KeyboardButton(text="да"),
            KeyboardButton(text="нет")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def choose_kb():
    kb = []
    row = [InlineKeyboardButton(text="По дате", callback_data='Выборпоиска По дате'),
           InlineKeyboardButton(text="По предмету", callback_data='Выборпоиска По предмету')]
    kb.append(row)
    row = [InlineKeyboardButton(text="По категории", callback_data='Выборпоиска По категории'),
           InlineKeyboardButton(text="Назад", callback_data='Выборпоиска Назад')]
    kb.append(row)
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return 'data' + ";" + ";".join([action, str(year), str(month), str(day)])


def calendar_kb(year=None, month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    # First row - Month and Year
    row = [InlineKeyboardButton(text=calendar.month_name[month] + " " + str(year), callback_data=data_ignore)]
    keyboard.append(row)
    # Second row - Week Days
    row = []
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        row.append(InlineKeyboardButton(text=day, callback_data=data_ignore))
    keyboard.append(row)
    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(text=str(day), callback_data=create_callback_data("DAY", year, month, day)))
        keyboard.append(row)
    # Last row - Buttons
    row = [InlineKeyboardButton(text="<", callback_data=create_callback_data("PREV-MONTH", year, month, day)),
           InlineKeyboardButton(text=" ", callback_data=data_ignore),
           InlineKeyboardButton(text=">", callback_data=create_callback_data("NEXT-MONTH", year, month, day))]
    keyboard.append(row)

    keyboard.append([InlineKeyboardButton(text="Назад", callback_data=create_callback_data("Выборпоиска",  year, month, day))])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def reply_kb(year=None, month=None):
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []

    row = []
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        row.append(KeyboardButton(text=day, callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(KeyboardButton(text=" ", callback_data=data_ignore))
            else:
                row.append(
                    KeyboardButton(text=str(day), callback_data=create_callback_data("DAY", year, month, day)))
        keyboard.append(row)

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def my_kb(b):
    kb = [
        [
            InlineKeyboardButton(text="Это моё", callback_data=f'МОЕ;{b}')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def prove_kb(b):
    keyboard = []
    row = [InlineKeyboardButton(text="ТОЧНО?", callback_data='не мое')]
    keyboard.append(row)
    row = [InlineKeyboardButton(text="Да", callback_data=f'МОЕ;{b};да'),
           InlineKeyboardButton(text="Нет", callback_data='МОЕ нет')]
    keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def reminder_kb(a):
    text1 = 'Напоминание;' + str(a) + ';Еще не успел'
    text2 = 'Напоминание;' + str(a) + ';Вещь не моя'
    kb = []
    row = [InlineKeyboardButton(text="Забрал", callback_data='Напоминание Забрал')]
    kb.append(row)
    row = [InlineKeyboardButton(text="Еще не успел", callback_data=text1)]
    kb.append(row)
    row = [InlineKeyboardButton(text="Вещь оказалась не моя", callback_data=text2)]
    kb.append(row)
    row = [InlineKeyboardButton(text="Другое", callback_data='Напоминание другое')]
    kb.append(row)
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def category_kb():
    kb = []
    category = ["одежда", "техника", "личные вещи", "украшения", "другое"]
    for i in category:
        row = [(InlineKeyboardButton(text=i, callback_data=f'Категория;{i}'))]
        kb.append(row)
    return InlineKeyboardMarkup(inline_keyboard=kb)


def category_choice_kb():
    kb = []
    category = ["одежда", "техника", "личные вещи", "украшения", "другое"]

    for i in category:
        row = [(KeyboardButton(text=i, callback_data=f'Категория {i}'))]
        kb.append(row)

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def check_kb(a):
    kb = []
    text1 = 'чат;' + a + ';да'
    text2 = 'чат;' + a + ';нет'
    row = [InlineKeyboardButton(text="✅ Принять", callback_data=text1), InlineKeyboardButton(text="❌ Отклонить", callback_data=text2)]
    kb.append(row)
    return InlineKeyboardMarkup(inline_keyboard=kb)
