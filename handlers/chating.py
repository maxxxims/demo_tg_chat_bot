from aiogram import types
from settings import dp, Messages, bot
from aiogram import Dispatcher
from keyboards import kb_gender, kb_skip, kb_topics
from FSM import Chatting
from aiogram.dispatcher import FSMContext
import database.user2user, database.user
from handlers.topics import send_topics
from typing import Any


async def send_to_companion(msg: types.Message, state = FSMContext):
    companion_id = await database.user2user.get_companion(str(msg.from_user.id))
    if companion_id is None:
        await Chatting.searching.set()
        await msg.answer(text='Идёт поиск собеседника...')
        return None
    await bot.send_message(companion_id, text=msg.text)


async def set_companion(msg: types.Message, state = FSMContext):
    if msg.text[0] == '/':
        return None
    companion_id = await database.user2user.get_companion(str(msg.from_user.id))
    if companion_id:
        await Chatting.next()
        await bot.send_message(companion_id, text=msg.text)
    else:
        await msg.answer(text='Идёт поиск собеседника...')


# async def stop(msg: types.Message, state = FSMContext):
#     await state.finish()
#     await msg.answer(text='Поиск прекращен')
#     await send_topics(msg)
#     companion = await database.user2user.get_companion(str(msg.from_user.id))
#     await bot.send_message(companion, text='Собеседник прекратил диалог, ищем другого...')
#     await database.user2user.stop_dialog(str(msg.from_user.id), companion)


def register_handlers_chatting(dp: Dispatcher):
    # dp.register_message_handler(stop, commands=['stop'], state=Any)
    dp.register_message_handler(set_companion, state=Chatting.searching)
    dp.register_message_handler(send_to_companion, state=Chatting.ongoing)