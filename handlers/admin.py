from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb, admin_to_kb
import datetime

ID = None


class FSMAdmin(StatesGroup):
    car_num = State()
    changes = State()
    photo = State()


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Нажмите на кнопку Добавить_Ремонт', reply_markup=admin_kb.button_case_admin_first_1)
    await message.delete()


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.car_num.set()
        await message.reply('Напишите гос. номер машины\n(только цифры)\nНапример: 540', reply_markup=admin_kb.button_case_admin_first_2)
        # await FSMAdmin.photo.set()
        # await message.reply('Загрузите фото', reply_markup=admin_kb.button_case_admin_first_2)


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK', reply_markup=admin_kb.button_case_admin_first_1)


async def skip_photo_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        # current_state = await state.get_state()
        # print(current_state)
        # if current_state is None:
        #     return
        #
        # async with state.proxy() as data:
        #     data[current_state] = 0
        async with state.proxy() as data:
            data['photo'] = 'AgACAgIAAxkBAAIG1mOEaT8_aZTAOMEoLeShXGmAUQABAQAC0sAxG4wDIUjY3DJYVqMBrwEAAwIAA3MAAysE'

        # if current_state == 'FSMAdmin:photo':
        #     await message.reply('Введите НОМЕР машины')
        # elif current_state == 'FSMAdmin:car_num':
        #     await message.reply('Что починили/заменили?')
        # await FSMAdmin.next()
        # data['photo'] = message.photo[0].file_id
        # await FSMAdmin.next()

        await sqlite_db.sql_add_command(state)
        await state.finish()
        await message.reply('Спасибо! Добавлена новая информация о ремонте ✅', reply_markup=admin_kb.button_case_admin_first_1)


async def load_car_num(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['car_num'] = int(message.text)
        await FSMAdmin.next()
        await message.reply('Напишите, что поменяли:', reply_markup=admin_kb.button_case_admin_first_2)


# async def load_car_num(message: types.Message, state: FSMContext):
#     if message.from_user.id == ID:
#         async with state.proxy() as data:
#             data['car_num'] = int(message.text)
#         await FSMAdmin.next()
#         await message.reply('Напишите, что поменяли:')


async def load_changes(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['changes'] = message.text
            data['time'] = datetime.datetime.now().strftime("%m.%d.%Y, %H:%M:%S")
        await FSMAdmin.next()
        await message.reply('Загрузите фото (если нужно):', reply_markup=admin_kb.button_case_admin_first_3)
        # await sqlite_db.sql_add_command(state)
        # await state.finish()


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        # await FSMAdmin.next()
        print(state)
        print(data)
        await sqlite_db.sql_add_command(state)
        await state.finish()
        await message.reply('Спасибо! Добавлена новая информация о ремонте ✅', reply_markup=admin_kb.button_case_admin_first_1)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Добавить_Ремонт_✅'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

    dp.register_message_handler(skip_photo_handler, state="*", commands='НЕ_Добавлять_Фото_❎')
    dp.register_message_handler(skip_photo_handler, Text(equals='Пропустить', ignore_case=True), state="*")

    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_car_num, state=FSMAdmin.car_num)
    dp.register_message_handler(load_changes, state=FSMAdmin.changes)
    # dp.register_message_handler(make_changes_command, commands=['Новый_Ремонт_❇️'], is_chat_admin=True)
    dp.register_message_handler(make_changes_command, commands=['Новый_Ремонт_❇️'])



#
# # --------------------------------------------------------------------------------------------------#
#
#
# class FSMAdmin_TO(StatesGroup):
#     car_num = State()
#     new_TO = State()
#
#
# # Получаем id модератора
# # @dp.message_handler(commands=['moderator'], is_chat_admin=True)
# async def make_TO_command(message: types.Message, state: FSMAdmin_TO):
#     global ID
#     ID = message.from_user.id
#     if message.from_user.id == ID:
#         await FSMAdmin_TO.car_num.set()
#         await bot.send_message(message.from_user.id, 'Укажите номер машины', reply_markup=admin_to_kb.button_case_admin)
#
#         current_state = await state.get_state()
#         print(current_state)
#         print('ok')
#         async with state.proxy() as data_TO:
#             data_TO['car_num'] = message.text
#         print('ok2')
#         await FSMAdmin_TO.next()
#         await message.reply('Введите когда новое ТО (км)')
#
#     await message.delete()
#
#
# # 5 Отмена
# # @dp.message_handler(state="*", commands='отмена')
# # @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
# async def cancel_TO_handler(message: types.Message, state: FSMAdmin_TO):
#     if message.from_user.id == ID:
#         current_state = await state.get_state()
#         if current_state is None:
#             return
#         await state.finish()
#         await message.reply('OK')
#
#
# # 4
# # @dp.message_handler(state=FSMAdmin.price)
# async def load_new_TO(message: types.Message, state: FSMAdmin_TO):
#     if message.from_user.id == ID:
#
#         current_state = await state.get_state()
#         print(current_state)
#
#         async with state.proxy() as data:
#             data['new_TO'] = int(message.text)
#         await sqlite_db.sql_add_command(state)
#         await state.finish()
#
#
# def register_handlers_admin_TO(dp: Dispatcher):
#     # dp.register_message_handler(make_TO_command, commands=['Обновить_ТО'], state=None)
#     dp.register_message_handler(cancel_TO_handler, state="*", commands='отмена')
#     dp.register_message_handler(cancel_TO_handler, Text(equals='отмена', ignore_case=True), state="*")
#
#     dp.register_message_handler(load_new_TO, state=FSMAdmin_TO.car_num)
#     dp.register_message_handler(make_TO_command, commands=['moderator2'], is_chat_admin=True)
#




# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram import types, Dispatcher
# from create_bot import dp, bot
# from aiogram.dispatcher.filters import Text
# from data_base import sqlite_db
# from keyboards import admin_kb
#
#
# ID = None
#
#
# class FSMAdmin(StatesGroup):
#     photo = State()
#     name = State()
#     description = State()
#     price = State()
#
#
# # Получаем id модератора
# # @dp.message_handler(commands=['moderator'], is_chat_admin=True)
# async def make_changes_command(message: types.Message):
#     global ID
#     ID = message.from_user.id
#     await bot.send_message(message.from_user.id, 'Что сделать хозяин?', reply_markup=admin_kb.button_case_admin)
#     await message.delete()
#
#
# # 0
# # @dp.message_handler(commands='Загрузить', state=None)
# async def cm_start(message: types.Message):
#     if message.from_user.id == ID:
#         await FSMAdmin.photo.set()
#         await message.reply('Загрузите фото')
#
#
# # 5 Отмена
# #@dp.message_handler(state="*", commands='отмена')
# #@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
# async def cancel_handler(message: types.Message, state: FSMContext):
#     if message.from_user.id == ID:
#         current_state = await state.get_state()
#         if current_state is None:
#             return
#         await state.finish()
#         await message.reply('OK')
#
#
# # 1
# # @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
# async def load_photo(message: types.Message, state: FSMContext):
#     if message.from_user.id == ID:
#         async with state.proxy() as data:
#             data['photo'] = message.photo[0].file_id
#         await FSMAdmin.next()
#         await message.reply('Теперь введите название')
#
#
# # 2
# # @dp.message_handler(state=FSMAdmin.photo)
# async def load_name(message: types.Message, state: FSMContext):
#     if message.from_user.id == ID:
#         async with state.proxy() as data:
#             data['name'] = message.text
#         await FSMAdmin.next()
#         await message.reply('Введите описание')
#
#
# # 3
# # @dp.message_handler(state=FSMAdmin.description)
# async def load_description(message: types.Message, state: FSMContext):
#     if message.from_user.id == ID:
#         async with state.proxy() as data:
#             data['description'] = message.text
#         await FSMAdmin.next()
#         await message.reply('Теперь укажите цену')
#
#
# # 4
# # @dp.message_handler(state=FSMAdmin.price)
# async def load_price(message: types.Message, state: FSMContext):
#     if message.from_user.id == ID:
#         async with state.proxy() as data:
#             data['price'] = float(message.text)
#         # async with state.proxy() as data:
#         #     await message.reply(str(data))
#         await sqlite_db.sql_add_command(state)
#         await state.finish()
#
#
#
#
#
# def register_handlers_admin(dp: Dispatcher):
#     dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
#     dp.register_message_handler(cancel_handler, state= "*", commands='отмена')
#     dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
#     dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
#     dp.register_message_handler(load_name, state=FSMAdmin.name)
#     dp.register_message_handler(load_description, state=FSMAdmin.description)
#     dp.register_message_handler(load_price, state=FSMAdmin.price)
#     dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)