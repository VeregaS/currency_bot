from aiogram.utils import executor
from start_bot import dp
from handlers import user, set_values, conversion, user_profile


user.register_handlers_user(dp)
user_profile.register_handlers_main_profile(dp)
set_values.register_handlers_set_values(dp)
conversion.register_handlers_conversion(dp)


if __name__ == '__main__':
    executor.start_polling(dp)
