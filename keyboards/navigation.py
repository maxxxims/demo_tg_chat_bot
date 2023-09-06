from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


button_anketa = KeyboardButton('/anketa')
button_stop = KeyboardButton('/stop')
button_next = KeyboardButton('/next')


kb_navigation = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_navigation.add(button_anketa).add(button_next).insert(button_stop)