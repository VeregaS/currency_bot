import sqlite3
from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.user import User_Dates
from keyboards import profile_main_page_keyboard, main_keyboard, profile_buttons_keyboard
from keyboards.profile_buttons_keyboard import valutes

conn = sqlite3.connect('db/Currency_bot.db', check_same_thread=False)
cursor = conn.cursor()


async def profile_main_page(call: types.CallbackQuery):
    keyboard = profile_main_page_keyboard.profile_main_keyboard_def()
    user_id = call.from_user.username
    data = cursor.execute(f"SELECT id, name, user_name, last_request FROM users WHERE name='{user_id}'").fetchall()[0]
    id = data[0]
    tg = data[1]
    name = data[2]
    last_request = data[3]
    if name == 'None':
        name = '-'
    await call.message.edit_text(f'ID: {id}\n'
                                 f'Tg: @{tg}\n'
                                 f'Имя: {name}\n'
                                 f'Последний запрос: {last_request}', reply_markup=keyboard)


async def back_to_main_page_fake(call: types.CallbackQuery):
    keyboard = main_keyboard.main_keyboard_def()
    user_name = call.from_user.username
    user_id = call.from_user.username
    data = cursor.execute(f"SELECT user_name FROM users WHERE name='{user_id}'").fetchall()[0]
    name = data[0]
    if 'None' in str(name):
        await call.message.edit_text(f"Привет, @{user_name}!\n", reply_markup=keyboard)
    else:
        await call.message.edit_text(f'Привет, {name}', reply_markup=keyboard)


async def change_name_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(f'Как вас зовут?')
    await state.set_state(User_Dates.name_changing.state)


async def change_name_end(message: types.Message, state: FSMContext):
    keyboard = main_keyboard.main_keyboard_def()
    name = message.text
    user_id = message.from_user.username
    cursor.execute(f"""UPDATE users SET user_name='{name}' WHERE name='{user_id}' """)
    conn.commit()
    await message.answer(f'Хорошее имя, {name}', reply_markup=keyboard)
    await state.finish()


async def change_buttons_start(call: types.CallbackQuery):
    user_id = call.from_user.username
    keyboard = profile_buttons_keyboard.new_buttons_keyboard_def(user_id)
    await call.message.edit_text(f'Выбери нужную валюту!', reply_markup=keyboard)


async def change_buttons_end(call: types.CallbackQuery):
    user_id = call.from_user.username
    choosen_valute = call.data.replace("curr_", "")
    data = cursor.execute(f"SELECT custom_buttons FROM users WHERE name='{user_id}'").fetchall()[0]
    user_buttons = list(data[0])
    index = valutes.index(choosen_valute)
    if user_buttons[index] == '0':
        user_buttons[index] = '1'
    else:
        user_buttons[index] = '0'
    new_user_buttons = ''.join(user_buttons)
    cursor.execute(f"""UPDATE users SET custom_buttons='{new_user_buttons}' WHERE name='{user_id}' """)
    conn.commit()
    keyboard = profile_buttons_keyboard.new_buttons_keyboard_def(user_id)
    await call.message.edit_text(f'Выбери нужную валюту!', reply_markup=keyboard)


def register_handlers_main_profile(dp: Dispatcher):
    dp.register_callback_query_handler(profile_main_page, lambda call: call.data == 'profile')
    dp.register_callback_query_handler(back_to_main_page_fake, lambda call: call.data == 'back_to_main_page')
    dp.register_callback_query_handler(change_name_start, lambda call: call.data == 'name_edit')
    dp.register_message_handler(change_name_end, state=User_Dates.name_changing)
    dp.register_callback_query_handler(change_buttons_start, lambda call: call.data == 'buttons_edit')
    dp.register_callback_query_handler(change_buttons_end, lambda call: str(call.data).startswith("curr_"))



