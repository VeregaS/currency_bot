import asyncio
from aiogram.utils import executor
from start_bot import dp
from handlers import user, set_values, user_profile


user.register_handlers_user(dp)
user_profile.register_handlers_main_profile(dp)
set_values.register_handlers_set_values(dp)


if __name__ == '__main__':
    executor.start_polling(dp)
