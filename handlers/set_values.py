import sqlite3
import requests
from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.user import User_Dates, ban

from keyboards import currency_keyboard, main_keyboard
from keyboards.profile_buttons_keyboard import valutes as currencys

conn = sqlite3.connect('db/Currency_bot.db', check_same_thread=False)
cursor = conn.cursor()


async def choose_origin_value_ask(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.username
    keyboard = currency_keyboard.currency_keyboard_def(user_id)
    custom_buttons = cursor.execute(f"SELECT custom_buttons FROM users WHERE name='{user_id}'").fetchall()[0][0]
    if custom_buttons != '0000000000':
        await call.message.answer('Выбирай нужную валюту и я скажу её курс!', reply_markup=keyboard)
        await state.set_state(User_Dates.waiting_origin_value.state)
    else:
        await call.message.answer(f'На данный момент курс RUB/RUB (рубль) составляет 1 рубль ^-^',
                                  reply_markup=types.ReplyKeyboardRemove())


async def choose_origin_value_answer(message: types.Message, state: FSMContext):
    await state.update_data(origin_value=message.text)
    currency = message.text
    if currency.upper() not in currencys:
        await message.answer(f'Я не понимаю что вы хотите этим сказать')
    else:
        user_id = message.from_user.username
        counter_request = int(cursor.execute(f"SELECT counter_request "
                                             f"FROM users WHERE name='{user_id}'").fetchall()[0][0])
        if int(counter_request) + 1 >= 5:
            await message.answer(f'Вы сделали 5 запросов за последнюю минуту. Вы получаете бан на 10 минут!')
            await ban(user_id, 10)
        else:
            cursor.execute(f"""UPDATE users SET counter_request='{str(int(counter_request) + 1)}'
             WHERE name='{user_id}' """)
            conn.commit()
            custom_buttons = cursor.execute(f"SELECT custom_buttons FROM users WHERE name='{user_id}'").fetchall()[0][0]
            cursor.execute(f"""UPDATE users SET last_request='{currency.upper()}' WHERE name='{user_id}' """)
            conn.commit()
            keyboard = main_keyboard.main_keyboard_def()
            user_id = message.from_user.username
            data = [str(i) for i in cursor.execute(f"SELECT last_request FROM users WHERE name='{user_id}'").fetchall()]
            valute = data[0].replace('(\'', '').replace("\',)", '')
            data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
            output_value_actual = data['Valute'][valute]['Value']
            output_value_past = data['Valute'][valute]['Previous']
            output_value_delta = output_value_actual - output_value_past
            output_value_name = data['Valute'][valute]['Name']
            output_value_code = data['Valute'][valute]['CharCode']
            p_delta, m_delta = '📈', '📉'
            currency_output_text = f'{"%.2f" % output_value_actual} '
            if output_value_delta > 0:
                currency_output_text += f'(+{"%.2f" % output_value_delta} {p_delta})'
            else:
                currency_output_text += f'(-{"%.2f" % output_value_delta} {m_delta})'

            await message.answer(f'На данный момент крус {output_value_code}/RUB ({output_value_name}) \n'
                                 f'составляет {currency_output_text}', reply_markup=keyboard)
        await state.finish()


def register_handlers_set_values(dp: Dispatcher):
    dp.register_callback_query_handler(choose_origin_value_ask, lambda call: call.data == 'check_currency')
    dp.register_message_handler(choose_origin_value_answer, state=User_Dates.waiting_origin_value)
