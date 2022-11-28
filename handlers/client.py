from aiogram import types, Dispatcher
from create_bot import dp, bot
# from keyboards import *
from keyboards import kb_client, kb_client_to
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Напишите в личку боту\nhttps://t.me/iceberg_to_bot')


async def command_list_cars(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Скоро ТО (меньше 5000) на следущие машины')  # reply_markup=ReplyKeyboardRemove())


async def command_soon_to(message: types.Message):
    await sqlite_db.sql_delta_to(message)


async def command_make_to(message: types.Message):
    await bot.send_message(message.from_user.id, 'Обновить ТО',
                           reply_markup=kb_client_to)  # reply_markup=ReplyKeyboardRemove())


async def garage_menu_command(message: types.Message):
    print(message)
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['helppp'])
    dp.register_message_handler(command_list_cars, commands=['Список_АВТО'])
    dp.register_message_handler(command_soon_to, commands=['Список_ТО_📃'])
    dp.register_message_handler(garage_menu_command, commands=['История_Работ_🛠️️'])
# @dp.message_handler()
# async def echo_send(message: types.Message):
#     await message.answer(message.text)
#     await message.reply(message.text)
#     await bot.send_message(message.from_user.id, message.text)
