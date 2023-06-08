import sqlite3
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import main_keyboard

conn = sqlite3.connect('db/Currency_bot.db', check_same_thread=False)
cursor = conn.cursor()


class User_Dates(StatesGroup):
    waiting_origin_value = State()
    name_changing = State()


async def start(message: types.Message):
    name = [str(i) for i in cursor.execute("SELECT name FROM users").fetchall()]
    user_name = message.from_user.username
    user_id = message.from_user.id
    user_name_check = f'(\'{user_name}\',)'
    if user_name_check not in name:
        cursor.execute('INSERT INTO users (id, name, custom_buttons) VALUES (?, ?, ?)',
                       (user_id, user_name, '0001100011'))
        conn.commit()
    data = cursor.execute(f"SELECT user_name FROM users WHERE name='{user_name}'").fetchall()[0]
    name = data[0]
    keyboard = main_keyboard.main_keyboard_def()
    if 'None' in str(name):
        await message.answer(f"Привет, @{user_name}!\n", reply_markup=keyboard)
    else:
        await message.answer(f'Привет, {name}', reply_markup=keyboard)


async def help(message: types.Message):
    await message.answer("Тут будет помощь!")


async def empety_message(msg: types.Message):
    keyboard = main_keyboard.main_keyboard_def()
    await msg.answer('Кнопки для кого придумали', reply_markup=keyboard)


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(empety_message)
