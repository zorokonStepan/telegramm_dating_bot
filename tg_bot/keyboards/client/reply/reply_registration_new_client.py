from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_over_bn = KeyboardButton(text="Начать с начала")

forth_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Далее").add(start_over_bn)
start_over_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(start_over_bn)
