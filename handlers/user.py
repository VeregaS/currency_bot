import sqlite3
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import main_keyboard

conn = sqlite3.connect('db/Currency_bot.db', check_same_thread=False)
cursor = conn.cursor()


class User_Dates(StatesGroup):
    waiting_origin_value = State()
    waiting_goal_value = State()


async def start(message: types.Message):
    id = [str(i) for i in cursor.execute("SELECT id FROM users").fetchall()]
    user_id = message.from_user.username
    user_id_check = f'(\'{user_id}\',)'
    if user_id_check not in id:
        cursor.execute('INSERT INTO users (id) VALUES (?)',
                       (user_id, ))
        conn.commit()
    keyboard = main_keyboard.main_keyboard_def()
    await message.answer(f"Привет, @{user_id}!\n",
                         reply_markup=keyboard)


async def help(message: types.Message):
    await message.answer("Выбери через кнопки какие валюты будем конвертировать!")


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
