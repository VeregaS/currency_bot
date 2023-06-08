import sqlite3
from aiogram import types

valutes = ['AUD', 'AZN', 'BYN', 'USD', 'JPY',
           'DKK', 'AMD', 'EGP', 'EUR', 'GBP']
yes, no = '✅', '❌'

conn = sqlite3.connect('db/Currency_bot.db', check_same_thread=False)
cursor = conn.cursor()


def new_buttons_keyboard_def(user_id):
    data = cursor.execute(f"SELECT custom_buttons FROM users WHERE name='{user_id}'").fetchall()[0]
    user_buttons = data[0]
    keyboard_main = types.InlineKeyboardMarkup(row_width=3)
    signs = []
    for elem in user_buttons:
        if elem == '0':
            signs.append(no)
        else:
            signs.append(yes)
    for i in range(2):
        buttons = [
            types.InlineKeyboardButton(f"{valutes[0 + 5 * i]} {signs[0 + 5 * i]}",
                                       callback_data=f"curr_{valutes[0 + 5 * i]}"),
            types.InlineKeyboardButton(f"{valutes[1 + 5 * i]} {signs[1 + 5 * i]}",
                                       callback_data=f"curr_{valutes[1 + 5 * i]}"),
            types.InlineKeyboardButton(f"{valutes[2 + 5 * i]} {signs[2 + 5 * i]}",
                                       callback_data=f"curr_{valutes[2 + 5 * i]}"),
            types.InlineKeyboardButton(f"{valutes[3 + 5 * i]} {signs[3 + 5 * i]}",
                                       callback_data=f"curr_{valutes[3 + 5 * i]}"),
            types.InlineKeyboardButton(f"{valutes[4 + 5 * i]} {signs[4 + 5 * i]}",
                                       callback_data=f"curr_{valutes[4 + 5 * i]}")]
        keyboard_main.add(*buttons)
    keyboard_main.add(types.InlineKeyboardButton(f'Назад', callback_data='profile'))
    return keyboard_main
