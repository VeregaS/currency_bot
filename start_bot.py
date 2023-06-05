from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='6196851031:AAET6Ti7h9LyJTXGSKjyPPBG-F0vy0IXxbU')
dp = Dispatcher(bot, storage=MemoryStorage())
