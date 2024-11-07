import asyncio
import logging
import sys
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# from pprint import pprint
from models import sort_by_data, send_data
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from keyboard import keyb, approve_kb, choose_kb, calendar_kb, reply_kb, my_kb, prove_kb, reminder_kb
from airtable import change_user_info, add_user, add_item_found, change_item_info
import datetime


# Bot token can be obtained via https://t.me/BotFather
# TOKEN = "7081007147:AAFx8B6HBYQ-o88bNjJbgwPKucbo-dw1vuA"

TOKEN = '8016908103:AAHV97jBuqlbPb3ehisB6Way0obvZGq71NE'


# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def on_startup(_):
    print('Бот был запущен')


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """

    add_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}! "
                         f"\n"
                         f"я бот для поиска потерянных вещей. Я помогу тебе найти твою потеряшку или передать вещь владельцу",
                         reply_markup=keyb()
                         )

@dp.message(F.text.lower() == 'я потерял кое-что')
async def approve(message: Message, state: FSMContext):
    change_user_info({'Пользователь': str(message.from_user.id), 'Искал или потерял': "потерял",
                      'когда обращался в последний раз': str(datetime.date.today())})
    try:
        answer = ('Выберите как вы будете искать вещь:\n\n'
                  'По дате: бот выдаст вам все найденные вещи, начиная с выбранной даты\n'
                  'По предмету: бот предложить все вещи из списка')
        await message.answer(answer, reply_markup=choose_kb())
    except:
        await message.answer('TROBLE')


class Form(StatesGroup):
    found_what = State()
    found_where = State()
    found_when = State()
    item_location = State()
    who_find = State()
    photo = State()
    confirmation = State()

# Получаем ответ на первый вопрос и задаем второй
# Обрабатываем фразу "я нашел кое-что"


@dp.message(F.text.lower() == "я нашел кое-что")
async def found_start(message: Message, state: FSMContext):
    change_user_info({'Пользователь': str(message.from_user.id), 'Искал или потерял': "нашел",
                      'когда обращался в последний раз': str(datetime.date.today())})
    await state.set_state(Form.found_what)  # Устанавливаем состояние
    await message.answer("Что ты нашел? Напиши что это за предмет.")  # Первый вопрос


@dp.message(Form.found_what)
async def process_found_where(message: Message, state: FSMContext):
    await state.update_data(found_what=message.text)  # Записываем ответ
    await state.set_state(Form.found_where)  # Переходим к следующему состоянию
    await message.answer("Где нашел? Где вещь была? Номер кабинета или корпус.")  # Второй вопрос
# Получаем ответ на первый вопрос и задаем второй


@dp.message(Form.found_where)
async def process_found_where(message: Message, state: FSMContext):
    await state.update_data(found_where=message.text)  # Записываем ответ
    await state.set_state(Form.found_when)  # Переходим к следующему состоянию
    await message.answer("Когда ты нашел?", reply_markup=reply_kb())  # Второй вопрос

# Получаем ответ на второй вопрос и задаем третий

@dp.message(Form.found_when)
async def process_found_when(message: Message, state: FSMContext):
    await state.update_data(found_when=f"{str(datetime.date.today())[0:7]}-{message.text}")  # Записываем ответ
    await state.set_state(Form.item_location)  # Переходим к следующему состоянию
    await message.answer("Где ты её оставил/оставишь?\nJОбычно вещи оставляют на пунктах охраны", reply_markup=ReplyKeyboardRemove())  # Третий вопрос


@dp.message(Form.item_location)
async def process_who_find(message: Message, state: FSMContext):
    await state.update_data(item_location=message.text)  # Записываем ответ
    await state.set_state(Form.photo)  # Переходим к следующему состоянию
    await message.answer("Отправь пожалуйста фото потерянной вещи")  # Третий вопрос


@dp.message(Form.photo)
async def process_photo(message: Message, state: FSMContext):
    # Сохраняем file_id фото
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await state.set_state(Form.who_find)  # Переходим к следующему состоянию
    await message.answer("Кто ты? Напиши свое Имя, чтобы если что владелец мог с тобой связаться")  # Третий вопрос

# Получаем ответ на третий вопрос и выводим все ответы


@dp.message(Form.who_find)
async def process_item_location(message: Message, state: FSMContext):
    await state.update_data(who_find=message.text)  # Записываем ответ

    # Получаем все данные, записанные в процессе диалога
    user_data = await state.get_data()

    response = (
        f"Итак, ты нашел - {user_data['found_what']}:\n"
        f"Где: {user_data['found_where']}\n"
        f"Когда: {user_data['found_when']}\n"
        f"Текущее местоположение: {user_data['item_location']}\n"
        f"Кто нашел: {user_data['who_find']}\n"
        f"Все верно?"
    )

    await message.answer(response, reply_markup=approve_kb())
    # Состояние подтверждение
    await state.set_state(Form.confirmation)


@dp.message(Form.confirmation)
async def process_confirmation(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        try:
            user_data = await state.get_data()
            r = []
            if user_data['found_when'].lower() == 'сегодня':
                r.append(datetime.date.today())
            change_user_info({'Имя': user_data['who_find'], 'Пользователь': str(message.from_user.id)})
            add_item_found({
                'Вещь': user_data["found_what"],
                'Где': user_data['found_where'],
                'Когда': user_data['found_when'],
                'Где сейчас': user_data['item_location'],
                'Пользователи': message.from_user.id,
                'PHOTO': user_data['photo']
            })
            await message.answer("Заявка создана", reply_markup=keyb())  # Убираем клавиатуру
            await state.clear()  # Завершаем машину состояний
        except:
            await message.answer("Давайте начнем заново.\nТы где-то допустил ошибку при заполнении, может указал дату не верно, или кинул фото где не нужно", reply_markup=keyb())  # Убираем клавиатуру
            await state.set_state(Form.found_where)  # Возвращаемся к первому вопросу
            await message.answer("Где ты нашел? Кабинет или корпус.")
    elif message.text.lower() == "нет":
        await message.answer("Давайте начнем заново.", reply_markup=keyb())  # Убираем клавиатуру
        await state.set_state(Form.found_where)  # Возвращаемся к первому вопросу
        await message.answer("Где ты нашел? Кабинет или корпус.")
    else:
        await message.answer("Пожалуйста, выбери 'Да' или 'Нет'.")

@dp.message()
async def wrong(message: Message):
    await message.answer('Я не понял тебя, если бот не работает попробуй написать команду /start')


@dp.callback_query()
async def callback(callback: types.CallbackQuery):
    if callback.data.startswith('Выборпоиска'):
        if callback.data.endswith('дате'):
            await callback.message.edit_text(text='Выбери дату', reply_markup=calendar_kb())
        elif callback.data.endswith('предмету'):
            await callback.message.edit_text(text='Выдает список потеряшек')
            for a, b, c in send_data():
                await callback.message.answer_photo(c)
                await callback.message.answer(a, reply_markup=my_kb(b))
        elif callback.data.endswith('Назад'):
            await callback.message.edit_text(text=f"Привет, {hbold(callback.message.from_user.full_name)}! "
                         "\nя могу подобрать тебе найти вещь или помочь тебе передать её владельцу")

    elif callback.data.startswith('МОЕ'):
        if callback.data.endswith('нет'):
            await callback.message.edit_text('Спасибо, что не забираешь чужое)')
        elif callback.data.endswith('да'):
            await callback.message.edit_text('Рад был помочь!\nПотом я у тебя узнаю вернул ты вещь или нет)')
            change_item_info(callback.data.split(';')[-2], str(callback.from_user.id))
            await kindly_reminder(callback.data.split(';')[-2], callback.from_user.id)
        else:
            await callback.message.edit_text(text="УВЕРЕН", reply_markup=prove_kb(callback.data.split(';')[-1]))

    elif callback.data.startswith('Напоминание'):
        if callback.data.endswith('Забрал'):
            await callback.message.edit_text('Я рад, что смог помочь)')
        elif callback.data.endswith("Еще не успел"):
            await callback.message.edit_text('я напомню попозже)')
            await kindly_reminder(callback.data.split(';')[1], callback.from_user.id)
        elif callback.data.endswith('Вещь не моя'):
            await callback.message.edit_text('Теперь вещь снова доступна в выдаче, надеюсь ты найдешь свое, а её владелец её')
            change_item_info(callback.data.split(';')[1], callback.from_user.id, status='нет')
        else:
            await callback.message.edit_text('Если у тебя возникла какая-то  проблема,то предлагаю связаться с моим создателем: '
                                             '@AMacedonsky')

    else:
        query = callback
        await callback.answer(callback.data)
        (_, action, year, month, day) = callback.data.split(';')
        curr = datetime.datetime(int(year), int(month), 1)
        if action == "IGNORE":
            await callback.message.answer(text='help', callback_query_id=callback.id)
        elif action == "DAY":
            await callback.message.edit_text(text='Тут появится выбор вещей потерянных по определенной дате')
            ret_data = True, datetime.date(int(year), int(month), int(day))
            for a, b, c in sort_by_data(ret_data):
                await callback.message.answer_photo(c)
                await callback.message.answer(a, reply_markup=my_kb(b))

        elif action == "PREV-MONTH":
            pre = curr - datetime.timedelta(days=1)
            await callback.message.edit_text(text=query.message.text,
                                          reply_markup=calendar_kb(int(pre.year), int(pre.month)))
        elif action == "NEXT-MONTH":
            ne = curr + datetime.timedelta(days=31)
            await callback.message.edit_text(text=query.message.text,
                                          reply_markup=calendar_kb(int(ne.year), int(ne.month)))
        elif action == "Выборпоиска":
            answer = ('Выберите как вы будете искать вещь:\n\n'
                      'По дате: бот выдаст вам все найденные вещи, начиная с определенной даты\n'
                      'По предмету: бот предложит вещи из списка')
            await callback.message.edit_text(answer, reply_markup=choose_kb())
        else:
            await callback.message.edit_text(callback_query_id=query.id, text="Something went wrong!")

async def kindly_reminder(item, user):
    await asyncio.sleep(15)
    await bot.send_message(user, 'Ты забрал потеряшку?', reply_markup=reminder_kb(item))



async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # And the run events dispatching
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
