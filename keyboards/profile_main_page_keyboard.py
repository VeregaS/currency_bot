from aiogram import types


def profile_main_keyboard_def():
    keyboard_main = types.InlineKeyboardMarkup()
    keyboard_main.add(types.InlineKeyboardButton(text='⚙️ㅤИзменить имяㅤ⚙️', callback_data="name_edit"))
    keyboard_main.add(types.InlineKeyboardButton(text='⚙️ㅤИзменить кнопкиㅤ⚙️', callback_data='buttons_edit'))
    keyboard_main.add(types.InlineKeyboardButton(text='↩ㅤНазадㅤ↩', callback_data='back_to_main_page'))
    return keyboard_main
