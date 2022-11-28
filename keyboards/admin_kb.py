from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

botton_load = KeyboardButton('/Загрузить')
button_cancel = KeyboardButton('/Отмена')
button_skip = KeyboardButton('/Пропустить')
button_delete = KeyboardButton('/Удалить')
button_skip_photo = KeyboardButton('/НЕ_Добавлять_Фото_❎')

button_new_fix = KeyboardButton('/Добавить_Ремонт_✅')
button_home = KeyboardButton('/На_Главное_меню_⬇️')

button_case_admin_first_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_new_fix).add(button_home)

button_case_admin_first_2 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)

button_case_admin_first_3 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_skip_photo)
# button_case_admin_first_3 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel).add(button_skip_photo)


# botton_load = KeyboardButton('/Загрузить')
# button_cancel = KeyboardButton('/Отмена')
# button_skip = KeyboardButton('/Пропустить')
# button_delete = KeyboardButton('/Удалить')
#
# button_case_admin_first = ReplyKeyboardMarkup(resize_keyboard=True).add(botton_load).add(button_cancel).\
#     add(button_skip).add(button_delete)