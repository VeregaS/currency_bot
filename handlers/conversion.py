import requests
import sqlite3
from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from pprint import pprint

import keyboards.main_keyboard
from handlers.user import User_Dates
from keyboards import main_keyboard

conn = sqlite3.connect('db/Currency_bot.db', check_same_thread=False)
cursor = conn.cursor()

api_key = "logiO6mnnnA1fFOo7ziBKqttC8hkMDBvH7a7hch0"


async def conversion_def_answer(call: types.CallbackQuery):
    keyboard = keyboards.main_keyboard.main_keyboard_def()
    user_id = call.from_user.username
    data = [str(i) for i in cursor.execute(f"SELECT lastrequest FROM users WHERE name='{user_id}'").fetchall()]
    valute = data[0].replace('(\'', '').replace("\',)", '')
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    output_value = data['Valute'][valute]['Value']
    output_value_name = data['Valute'][valute]['Name']
    output_value_code = data['Valute'][valute]['CharCode']
    await call.message.edit_text(f'На данный момент крус {output_value_code} ({output_value_name}) \n'
                                 f'составляет {output_value}', reply_markup=keyboard)


async def user_says_no(call: types.CallbackQuery):
    keyboard = keyboards.main_keyboard.main_keyboard_def()
    await call.message.edit_text(f'Ну на нет и дела нет', reply_markup=keyboard)


def register_handlers_conversion(dp: Dispatcher):
    dp.register_callback_query_handler(conversion_def_answer, lambda call: call.data == 'yes')
    dp.register_callback_query_handler(user_says_no, lambda call: call.data == 'no')
