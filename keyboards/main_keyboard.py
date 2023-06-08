from aiogram import types


def main_keyboard_def():
    keyboard_main = types.InlineKeyboardMarkup()
    keyboard_main.add(types.InlineKeyboardButton(text="Курс валют", callback_data="check_currency"))
    keyboard_main.add(types.InlineKeyboardButton(text='Профиль', callback_data='profile'))
    return keyboard_main
