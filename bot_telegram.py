from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other, admin_TO
from data_base import sqlite_db


async def on_startup(_):
    print('Бот активирован')
    sqlite_db.sql_start()

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
admin_TO.register_handlers_admin_TO(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
