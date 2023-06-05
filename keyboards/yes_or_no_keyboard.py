from aiogram import types


def y_or_n_keyboard_def():
    keyboard_y_or_n = types.InlineKeyboardMarkup()
    keyboard_y_or_n.add(types.InlineKeyboardButton(text="Да", callback_data="yes"))
    keyboard_y_or_n.add(types.InlineKeyboardButton(text="Нет", callback_data="no"))
    return keyboard_y_or_n
