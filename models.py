from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegramcalendar import create_calendar, process_calendar_selection
import datetime
from pprint import pprint
import aiogram.utils as utils
from airtable import get_item, get_users_data


def create_datatime(date):
    a, b, c = date['fields']['Когда'].split('-')
    return datetime.date(int(a), int(b), int(c))


def sort_by_data(ret_data):
    _, data = ret_data
    data_list = get_item()
    lists = []
    for i in data_list:
        date = create_datatime(i)
        if date >= data:
            lists.append(i)
    return send_data(lists)


def send_data(lists=None):
    if lists is None:
        data = get_item()
    else:
        data = lists
    users = get_users_data()

    row = []
    for i in data:
        a = i['fields']
        b = a['Когда'].split('-')
        for user in users:
            if user['id'] == i['fields']['Пользователи'][0]:
                if i['fields']['Найдена'] == 'нет':
                    try:
                        text = f'Потеряшка: {a["Вещь"]}' \
                               f'\nБыла найдена в {a["Где"]}  {b[-1]} числа {b[1]}.{b[0]}' \
                               f'\nНашел её {user["fields"]["Имя"]} - можешь написать ему по повожу вещи в ЛС @{user["fields"]["ник"]}' \
                               f'\nСейчас потеряшка в {a["Где сейчас"]}'
                        row.append((text, i['id'], a['PHOTO']))
                    except:
                        try:
                            text = f'Потеряшка: {a["Вещь"]}' \
                                   f'\nБыла найдена в {a["Где"]}  {b[-1]} числа {b[1]}.{b[0]}' \
                                   f'\nНашел её {user["fields"]["Имя"]}' \
                                   f'\nСейчас потеряшка в {a["Где сейчас"]}'
                            row.append((text, i['id'], a['PHOTO']))
                        except:
                            text = 'Ошибка'
                            row.append((text, i['id']))
    return row

