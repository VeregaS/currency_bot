import sqlite3
from aiogram import types
from start_bot import dp, bot
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.user import User_Dates
from keyboards import currency_keyboard, yes_or_no_keyboard
from keyboards.currency_keyboard import currencys


conn = sqlite3.connect('db/Currency_bot.db', check_same_thread=False)
cursor = conn.cursor()


async def choose_origin_value_ask(call: types.CallbackQuery, state: FSMContext):
    keyboard = currency_keyboard.currency_keyboard_def()
    await call.message.answer('Выбирай нужную валюту и я скажу её курс!', reply_markup=keyboard)
    await state.set_state(User_Dates.waiting_origin_value.state)


async def choose_origin_value_answer(message: types.Message, state: FSMContext):
    await state.update_data(origin_value=message.text)
    origin_currency = message.text
    if origin_currency.upper() not in currencys:
        await message.answer(f'{origin_currency} - такой валюты я ещё не слышал :(')
    else:
        keyboard = yes_or_no_keyboard.y_or_n_keyboard_def()
        user_id = message.from_user.username
        cursor.execute(f"""UPDATE users SET lastrequest='{origin_currency.upper()}' WHERE name='{user_id}' """)
        conn.commit()
        await message.answer(f'Тебя интересует {origin_currency}?', reply_markup=types.ReplyKeyboardRemove())
        # await bot.edit_message_reply_markup(chat_id=message.from_user.id,
        #                                     message_id=message.message_id,
        #                                     reply_markup=keyboard)
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id,
                                            reply_markup=keyboard)
        await state.finish()


def register_handlers_set_values(dp: Dispatcher):
    dp.register_callback_query_handler(choose_origin_value_ask, lambda call: call.data == 'origin')
    dp.register_message_handler(choose_origin_value_answer, state=User_Dates.waiting_origin_value)
