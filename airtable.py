from pyairtable import Api
# from pprint import pprint


api = Api('patSxQtpMd6a4iKOq.83e528e67458f9fbce584126c80b9f5fd518401f5aa629591a7264ecbba04082')


DB_ID = 'appeNb48kX0169buS'
item_id = 'tblS4WhViKaVEWkcO'
users_id = 'tblVQ1TvSKcuT8j9f'
dop_id = 'tbla915OURYq9LpdB'


item_table = api.table(DB_ID, item_id)
user_table = api.table(DB_ID, users_id)
dop_table = api.table(DB_ID, dop_id)


def get_dop():
    return dop_table.all()


def get_item():
    return item_table.all()


def get_users_data():
    return user_table.all()


def add_dop(param):
    data = get_dop()
    for i in data:
        if i['fields']['Name'] == param:
            c = int(i['fields']['количество кликов'])
            c += 1
            dop_table.update(i['id'], {'количество кликов': str(c)})
            return True


def add_user(id, nick):
    """
    Добавляет пользователя в бд по первому сообщению
    :param id: уникальный номер в телеграмме
    :param nick: никнейм пользователя
    :return:
    """
    list_data = get_users_data()
    for i in list_data:
        if i['fields']['Пользователь'] == str(id):
            user_table.update(i['id'], {'ник': nick})
            return True
    user_table.create({'Пользователь': str(id), "ник": nick})


def add_item_found(data: dict):
    list_data = get_users_data()
    dat = data
    for i in list_data:
        if i['fields']['Пользователь'] == str(data['Пользователи']):
            dat['Пользователи'] = [i['id']]
            item_table.create(data)
            return 'Успех'


def change_item_info(id, user, status='да'):
    list_data = get_item()
    users = get_users_data()
    for i in list_data:
        if i['id'] == str(id):
            for a in users:
                if a['fields']['Пользователь'] == str(user):
                    item_table.update(i['id'], {'Пользователи 2': [str(a['id'])], 'Найдена': status})


def approve_item(id, param):
    list_data = get_item()
    for i in list_data:
        if i['id'] == str(id):
            item_table.update(i['id'], {param[0]: param[1]})


def delet_id(id):
    list_data = get_item()
    for i in list_data:
        if i['id'] == str(id):
            item_table.delete(i['id'])


def change_user_info(data: dict):
    list_data = get_users_data()
    for i in list_data:
        if i['fields']['Пользователь'] == data['Пользователь']:
            user_table.update(i['id'], data)
            return True


# if __name__ == "__main__":
    # pprint(get_item())
    # pprint(get_users_data())
    # add_user('666', 'roma')

    # d  = {
    #     'Вещь': 'Телефон',
    #     'Где': 'дома',
    #     'Когда': '2024-09-08',
    #     'Где сейчас': 'у меня',
    #     'Пользователи': '222',
    #     # 'Нашли (from Пользователи)': '222'
    # }
    #
    # pprint(add_item_found(d))

    # d = {
    #     'нашел?': 'да',
    #     'ник': 'мут',
    #     'Искал или потерял': 'искал',
    #     'когда обращался в последний раз': '2024-12-08',
    #     'Пользователь': '555',
    # }
    # pprint(change_user_info(d))

    # pprint(section_table.all())
    # pprint(api.base("appeNb48kX0169buS"))
# table.all()
# [
#     {
#         "id": "rec5eR7IzKSAOBHCz",
#         "createdTime": "2017-03-14T22:04:31.000Z",
#         "fields": {
#             "Name": "Alice",
#             "Email": "alice@example.com"
#         }
#     }
# ]
# table.create({"Name": "Bob"})
# {
#     "id": "recwAcQdqwe21asdf",
#     "createdTime": "...",
#     "fields": {"Name": "Bob"}
# }
# table.update("recwAcQdqwe21asdf", {"Name": "Robert"})
# {
#     "id": "recwAcQdqwe21asdf",
#     "createdTime": "...",
#     "fields": {"Name": "Robert"}
# }
# table.delete("recwAcQdqwe21asdf")
# {'id': 'recwAcQdqwe21asdf', 'deleted': True}
