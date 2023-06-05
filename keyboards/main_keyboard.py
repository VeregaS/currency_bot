from aiogram import types


def main_keyboard_def():
    keyboard_main = types.InlineKeyboardMarkup()
    keyboard_main.add(types.InlineKeyboardButton(text="Начать", callback_data="origin"))
    return keyboard_main
