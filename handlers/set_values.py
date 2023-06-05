import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.user import User_Dates
from keyboards import currency_keyboard, main_keyboard, yes_or_no_keyboard
from aiogram.contrib.fsm_storage.memory import MemoryStorage

conn = sqlite3.connect('db/Currency_bot.db', check_same_thread=False)
cursor = conn.cursor()


async def choose_origin_value_ask(call: types.CallbackQuery, state: FSMContext):
    keyboard = currency_keyboard.currency_keyboard_def()
    await call.message.answer('Напиши сумму и валюту которую будем конвертировать (валюты предложены в кнопках).'
                              'Пример: 100 RUB',
                              reply_markup=keyboard)
    await state.set_state(User_Dates.waiting_origin_value.state)


async def choose_origin_value_answer(message: types.Message, state: FSMContext):
    await state.update_data(origin_value=message.text)
    origin_currency = message.text
    keyboard = currency_keyboard.currency_keyboard_def()
    await state.set_state(User_Dates.waiting_goal_value.state)
    await message.answer(f'Хорошо, так и запишем, {origin_currency}. В какую валюту это конвертируем? ',
                         reply_markup=keyboard)


async def choose_goal_value_answer(message: types.Message, state: FSMContext):
    goal_currency = message.text
    user_data = await state.get_data()
    user_id = message.from_user.username
    keyboard = yes_or_no_keyboard.y_or_n_keyboard_def()
    cursor.execute(f"""UPDATE users SET origin='{user_data["origin_value"]}' WHERE id='{user_id}' """)
    conn.commit()
    cursor.execute(f"""UPDATE users SET goal='{goal_currency}' WHERE id='{user_id}' """)
    conn.commit()
    await message.answer(f'Конвертируем {user_data["origin_value"]} в {goal_currency}?', reply_markup=keyboard)


def register_handlers_set_values(dp: Dispatcher):
    dp.register_callback_query_handler(choose_origin_value_ask, lambda call: call.data == 'origin')
    dp.register_message_handler(choose_origin_value_answer, state=User_Dates.waiting_origin_value)
    dp.register_message_handler(choose_goal_value_answer, state=User_Dates.waiting_goal_value)
