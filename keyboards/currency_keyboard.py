from aiogram import types


def currency_keyboard_def():
    keyboard_currency = types.ReplyKeyboardMarkup(resize_keyboard=True)
    currencys = ["USD", "EUR", "GBP", "JPY", "RUB"]
    keyboard_currency.add(*currencys)
    return keyboard_currency
