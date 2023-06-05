import yahoo_fin.stock_info as si
from datetime import datetime, timedelta
import sqlite3
from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards import main_keyboard

conn = sqlite3.connect('db/Currency_bot.db', check_same_thread=False)
cursor = conn.cursor()


def convert(src, dst, amount):
    symbol = f"{src}{dst}=X"
    latest_data = si.get_data(symbol, interval="1m", start_date=datetime.now() - timedelta(days=2))
    last_updated_datetime = latest_data.index[-1].to_pydatetime()
    latest_price = latest_data.iloc[-1].close
    return last_updated_datetime, latest_price * amount


async def conversion_def_answer(call: types.CallbackQuery):
    keyboard = main_keyboard.main_keyboard_def()
    user_id = call.from_user.username
    data = [str(i) for i in cursor.execute(f"SELECT origin, goal FROM users WHERE id='{user_id}'").fetchall()]
    origin = str(data[0].split("\', \'")[0])[2:]
    money = int(origin.split()[0])
    currency_origin = str(origin.split()[1])
    currency_goal = str(data[0].split("\', \'")[1])[:-2]
    time, resault = convert(currency_origin, currency_goal, money)
    await call.message.edit_text(f'На {str(str(time).split()[0]).replace("-", " ")} выходит что:\n'
                              f'{money} {currency_origin} = {"%.2f" % resault} {currency_goal}', reply_markup=keyboard)


def register_handlers_conversion(dp: Dispatcher):
    dp.register_callback_query_handler(conversion_def_answer, lambda call: call.data == 'yes')
