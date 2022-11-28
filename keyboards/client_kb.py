from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Менюю')
b2 = KeyboardButton('/Список_АВТО')
b3 = KeyboardButton('/Список_ТО')
b4 = KeyboardButton('/Пройти_ТО')
# b4 = KeyboardButton('Поделиться номером', request_contact=True)
# b5 = KeyboardButton('Отправить где я', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).row(b2, b3).row(b4)


button_car_num = KeyboardButton('/Выбрать_Машину')
button_home = KeyboardButton('/Главное_меню')

kb_client_to = ReplyKeyboardMarkup(resize_keyboard=True).add(button_car_num).add(button_home)

