from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_cancel = KeyboardButton('/Отмена_')
button_car_num = KeyboardButton('/Выбрать_Машину_🚚')
button_home = KeyboardButton('/На_Главное_меню_⬇️')

button_case_admin_to_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_car_num).add(button_home)
button_case_admin_to_2 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel).add(button_car_num)


m1 = KeyboardButton('/История_Работ_🛠️️')
m2 = KeyboardButton('/Список_ТО_📃')
m3 = KeyboardButton('/Новый_Ремонт_❇️')
m4 = KeyboardButton('/Обновить_ТО_❇️')
# b4 = KeyboardButton('Поделиться номером', request_contact=True)
# b5 = KeyboardButton('Отправить где я', request_location=True)

kb_to_main = ReplyKeyboardMarkup(resize_keyboard=True).row(m1, m2).row(m3, m4)  # .row(b4,b5)

# m1 = KeyboardButton('/Меню')
# m2 = KeyboardButton('/Список_АВТО')
# m3 = KeyboardButton('/Новый_Ремонт')
# m4 = KeyboardButton('/Обновить_ТО')
# # b4 = KeyboardButton('Поделиться номером', request_contact=True)
# # b5 = KeyboardButton('Отправить где я', request_location=True)
#
# kb_to_main = ReplyKeyboardMarkup(resize_keyboard=True).add(m1).row(m2, m3).row(m4)  # .row(b4,b5)
