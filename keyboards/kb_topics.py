# send kb with topics
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import database.user2user


async def get_kb_topics() -> InlineKeyboardMarkup:
    kb_topics = InlineKeyboardMarkup(row_width=3)
    topics_to_users = await database.user2user.get_users_by_topics()
    for topic in topics_to_users:


kb_topics = InlineKeyboardMarkup(row_width=3)

kb_topics.add(
    InlineKeyboardButton('Исскуство', callback_data='set_topic_art'),
    InlineKeyboardButton('Спорт', callback_data='set_topic_sport'),
    InlineKeyboardButton('Политика', callback_data='set_topic_politics'),
    InlineKeyboardButton('Юмор', callback_data='set_topic_humor'),
    InlineKeyboardButton('Наука', callback_data='set_topic_science'),
    InlineKeyboardButton('Религия', callback_data='set_topic_religion')
)