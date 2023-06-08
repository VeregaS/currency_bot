import sqlite3
from aiogram import types
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.profile_buttons_keyboard import valutes

conn = sqlite3.connect('db/Currency_bot.db', check_same_thread=False)
cursor = conn.cursor()


def currency_keyboard_def(user_id):
    data = cursor.execute(f"SELECT custom_buttons FROM users WHERE name='{user_id}'").fetchall()[0]
    user_buttons = data[0]
    if user_buttons != '0000000000':
        currencys = [str(i) for i in valutes if user_buttons[valutes.index(i)] == '1']
        keyboard_currency = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        fix = 0
        for i in range(0, len(currencys) - 1, 2):
            keyboard_currency.add(currencys[i], currencys[i + 1])
            fix += 2
        if fix != len(currencys):
            keyboard_currency.add(currencys[len(currencys) - 1])
    else:
        keyboard_currency = types.ReplyKeyboardRemove()
    return keyboard_currency
