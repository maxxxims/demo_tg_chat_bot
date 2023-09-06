from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


kb_skip = InlineKeyboardMarkup(row_width=3)
kb_skip.add(InlineKeyboardButton('Пропустить', callback_data="skip"))