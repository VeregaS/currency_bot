from aiogram import types
currencys = ["USD", "EUR", "GBP", "JPY", "RUB"]


def currency_keyboard_def():
    keyboard_currency = types.ReplyKeyboardMarkup(resize_keyboard=True)
    fix = 0
    for i in range(0, len(currencys) - 1, 2):
        keyboard_currency.add(currencys[i], currencys[i + 1])
        fix += 2
    if fix != len(currencys):
        keyboard_currency.add(currencys[len(currencys) - 1])
    return keyboard_currency
