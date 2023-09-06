import os
from aiogram import Bot, Dispatcher, executor, types
# from aiogram.types import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from settings import dp, bot, create_tables, drop_tables
from handlers import commands, registration, topics, chating


# models.user.Base.metadata.create_all(bind=engine)


commands.register_handlers_commands(dp)
registration.register_handlers_registration(dp)
topics.register_handlers_topics(dp)
chating.register_handlers_chatting(dp)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=create_tables, on_shutdown=drop_tables)


# сделать кнопки для навигации +
# изменить кнопку анкета +
# обработать окончание диалога (разнести по разным функциям) +
# вынести комаду для анкеты в команды +
# темы с отображением количества человек в них