import datetime
import logging
from airtable import get_item, get_users_data, change_user_info


def create_datatime(date):
    a, b, c = date['fields']['Когда'].split('-')
    return datetime.date(int(a), int(b), int(c))


def time_count(id):
    data = get_users_data()
    delta = datetime.datetime.now()
    for i in data:
        if i['fields']['Пользователь'] == str(id):
            ti = i['fields']['Время начала']
            a, b = ti.split(' ')
            c, d, e = a.split('-')
            f, g, z = b.split(':')
            z = z.split('.')[0]
            time = datetime.datetime(int(c), int(d), int(e), int(f), int(g), int(z))
            delta = delta - time
            change_user_info({'Пользователь': str(id), 'Время использования бота': str(delta)})


def categoty(word):
    data = get_item()
    lists = []
    for i in data:
        if i['fields']['Категория'] == word:
            lists.append(i)
    return send_data(lists)


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
                if i['fields']['Найдена'] == 'нет' and i['fields']['Одобрено'] == 'да':
                    try:
                        text = f'Потеряшка: <b>{a["Вещь"]}</b>' \
                               f'\nБыла найдена в {a["Где"]}  {b[-1]} числа {b[1]}.{b[0]}' \
                               f'\nНашел её {user["fields"]["Имя"]} - можешь написать ему по поводу вещи в ЛС @{user["fields"]["ник"]} ' \
                               f'\nСейчас потеряшка в {a["Где сейчас"]}'
                        row.append((text, i['id'], a['PHOTO']))
                    except Exception as e:
                        logging.error(e)
                        try:
                            text = f'Потеряшка: <b>{a["Вещь"]}</b>' \
                                   f'\nБыла найдена в {a["Где"]}  {b[-1]} числа {b[1]}.{b[0]}' \
                                   f'\nНашел её {user["fields"]["Имя"]}' \
                                   f'\nСейчас потеряшка в {a["Где сейчас"]}'
                            row.append((text, i['id'], a['PHOTO']))
                        except Exception as e:
                            logging.error(e)
                            text = f'Ошибка {a["Вещь"]}'
                            row.append((text, i['id'], a['PHOTO']))
    return row
