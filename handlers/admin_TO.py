from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb, admin_to_kb
import datetime


ID = None


class FSMAdmin_TO(StatesGroup):
    car_num = State()
    new_TO = State()


#
# async def make_TO_command(message: types.Message):
#     global ID
#     ID = message.from_user.id
#     await bot.send_message(message.from_user.id, 'Укажите номер машины', reply_markup=admin_to_kb.button_case_admin)
#     await FSMAdmin_TO.car_num.set()
#     await message.delete()
#
#     print('a')
#     # await FSMAdmin_TO.next()

async def make_TO_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Обновляем ТО:', reply_markup=admin_to_kb.button_case_admin_to_1)
    await message.delete()


# 0
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start_TO(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin_TO.car_num.set()
        await message.reply('Напишите гос. номер машины\n(только цифры)\nНапример: 540', reply_markup=admin_to_kb.button_case_admin_to_2)
        # await message.delete()


# 5 Отмена
async def cancel_TO_handler(message: types.Message, state: FSMAdmin_TO):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        # await bot.send_message(message.from_user.id, 'o', reply_markup=admin_to_kb.button_case_admin_to_1)
        await state.finish()
        # await message.delete()
        await message.reply('Обновляем ТО:', reply_markup=admin_to_kb.button_case_admin_to_1)


async def load_new_car(message: types.Message, state: FSMAdmin_TO):
    if message.from_user.id == ID:
        # current_state = await state.get_state()
        async with state.proxy() as data_TO:
            data_TO['car_num'] = int(message.text)
        await FSMAdmin_TO.next()
        await message.reply('Введите когда новое ТО (км)', reply_markup=admin_to_kb.button_case_admin_to_2)

    # await message.delete()


# 4
async def load_new_TO(message: types.Message, state: FSMAdmin_TO):
    if message.from_user.id == ID:
        current_state = await state.get_state()

        async with state.proxy() as data:
            data['new_TO'] = int(message.text)
            data['time'] = datetime.datetime.now().strftime("%m.%d.%Y, %H:%M:%S")

        await message.reply('Спасибо, ТО обновлено ✅', reply_markup=admin_to_kb.button_case_admin_to_1)
        await sqlite_db.sql_update(state, data['new_TO'], data['car_num'], data['time'])

        async with state.proxy() as data2:
            data2['car_num'] = data['car_num']
            data2['time'] = data['time']
            add_data_new_TO = data['new_TO']
            # data2['changes'] = f'Новое_ТО {add_data_new_TO}'
            data2['photo'] = 'AgACAgIAAxkBAAIGAAFjhGJNBDYPtOqIb2tT7Z7DIReZ8wACpMAxG4wDIUgXPbAlyafpvwEAAwIAA3MAAysE'

        await sqlite_db.sql_add_command(state)

        await state.finish()


async def TO_main_menu_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Главное Меню:', reply_markup=admin_to_kb.kb_to_main)
    await message.delete()


async def new_service(message: types.Message):
    await bot.send_message(message.from_user.id, 'Новый Ремонт:', reply_markup=admin_kb.button_case_admin_first_1)
    await message.delete()


def register_handlers_admin_TO(dp: Dispatcher):
    # dp.register_message_handler(make_TO_command, commands=['Загрузить'], state=None)

    # dp.register_message_handler(make_TO_command, commands=['Обновить_ТО'], state=None)
    dp.register_message_handler(cm_start_TO, commands=['Выбрать_Машину_🚚'], state=None)

    dp.register_message_handler(cancel_TO_handler, state="*", commands='Отмена_')
    dp.register_message_handler(cancel_TO_handler, Text(equals='Отмена_', ignore_case=True), state="*")

    dp.register_message_handler(load_new_car, state=FSMAdmin_TO.car_num)
    dp.register_message_handler(load_new_TO, state=FSMAdmin_TO.new_TO)

    dp.register_message_handler(TO_main_menu_command, commands=['start', 'help', 'На_Главное_меню_⬇️'], state=None)

    # dp.register_message_handler(make_TO_command, commands=['m2', 'Обновить_ТО'], is_chat_admin=True)
    dp.register_message_handler(make_TO_command, commands=['m2', 'Обновить_ТО_❇️'])
    dp.register_message_handler(new_service, commands=['Новый_Ремонт_❇️'])
