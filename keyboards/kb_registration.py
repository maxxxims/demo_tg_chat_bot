from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


button_continue = KeyboardButton('/continue')


kb_registration = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_registration.add(button_continue)



# INLINE
kb_gender = InlineKeyboardMarkup(row_width=3)
kb_gender.add(InlineKeyboardButton('Мужской', callback_data="set_gender_male"), 
              InlineKeyboardButton('Женский', callback_data="set_gender_female"),
              InlineKeyboardButton('Пропустить', callback_data="set_gender_skip"))
