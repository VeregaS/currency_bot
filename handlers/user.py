import sqlite3
import asyncio
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
    if user_name is None or 'None' in user_name:
        user_name = user_id
    user_name_check = f'(\'{user_name}\',)'
    if user_name_check not in name:
        cursor.execute(
            'INSERT INTO users (id, name, custom_buttons, counter_request, is_banned) VALUES (?, ?, ?, ?, ?)',
            (user_id, user_name, '0001100011', 0, 0))
        conn.commit()
    data = cursor.execute(f"SELECT user_name FROM users WHERE name='{user_name}'").fetchall()[0]
    name = data[0]
    keyboard = main_keyboard.main_keyboard_def()
    loop = asyncio.get_event_loop()
    loop.create_task(counter_request_to_0(user_name, 60))
    if 'None' in str(name):
        await message.answer(f"Привет, @{user_name}!\n", reply_markup=keyboard)
    else:
        await message.answer(f'Привет, {name}', reply_markup=keyboard)


async def help(message: types.Message):
    await message.answer("Просто используй кнопки и не делай 5 и больше запросов в минуту :)")


async def empety_message(message: types.Message):
    keyboard = main_keyboard.main_keyboard_def()
    await message.answer('Используйте кнопки для взаимодействия со мной!', reply_markup=keyboard)


async def counter_request_to_0(user_id, time_counter):
    await asyncio.sleep(time_counter)
    counter_request = 0
    cursor.execute(
        f"""UPDATE users SET counter_request='{counter_request}' WHERE name='{user_id}' """)
    conn.commit()


async def ban(user_id, ban_time):
    is_banned = int(cursor.execute(f"SELECT is_banned "
                                   f"FROM users WHERE name='{user_id}'").fetchall()[0][0])
    if is_banned != 1:
        cursor.execute(
            f"""UPDATE users SET is_banned='{1}' WHERE name='{user_id}' """)
        conn.commit()
        await asyncio.sleep(ban_time)
        cursor.execute(
            f"""UPDATE users SET is_banned='{0}' WHERE name='{user_id}' """)
        conn.commit()
        cursor.execute(
            f"""UPDATE users SET counter_request='{0}' WHERE name='{user_id}' """)
        conn.commit()


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(empety_message)
