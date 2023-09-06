from aiogram import types
from settings import dp, Messages, engine, Base, bot
from aiogram import Dispatcher
from keyboards import kb_registration, kb_navigation, kb_topics
from aiogram.types import ReplyKeyboardRemove
from aiohttp import request
import database.user, database.user2user
from aiogram.dispatcher import FSMContext
from FSM import Registration, Chatting
from handlers.topics import send_topics
from logic.anketa import make_anketa
from logic.companions import find_companion


async def start(msg: types.Message):
    await msg.answer(text=Messages.start, reply_markup=kb_navigation)


async def anketa(msg: types.Message, state = None):
    user = await database.user.get_user(str(msg.from_user.id))
    if user is None:
        await Registration.name.set()
        await msg.answer(text=f'Введите имя, которое увидят ваши собеседники')
    else:
        users_anketa = make_anketa(user)
        await msg.answer(f'Ваша анкета:\n{users_anketa}')


async def stop(message: types.Message, state: FSMContext):
    user_info = await database.user2user.get_user_info(str(message.from_user.id))
    if user_info is None:
        await message.answer(text='Вы еще не начали поиск!')
    elif user_info.companion is None and user_info.is_searching is True:
        await state.finish()
        # add is_searching FALSE  
        await database.user2user.stop_user_expectation(str(message.from_user.id))  
        await message.answer(text='Поиск прекращен')
    elif await state.get_state() in Registration:
        await state.finish()
        await message.answer(text='Заполнение анкеты приостановлено')
    elif user_info.companion is not None:
        # to user
        await message.answer(text='Вы прекратили диалог')
        await state.finish()
        await send_topics(message)
        # to companion
        # find companion
        print(f'**************** {user_info.companion}')
        await bot.send_message(user_info.companion, text='Собеседник прекратил диалог, ищем другого...',
                               reply_markup=kb_navigation)
        await database.user2user.stop_dialog(str(message.from_user.id), user_info.companion)
        await find_companion(str(user_info.companion), user_info.topic)


async def topic(msg: types.Message, state: FSMContext = None):
    print('here', await state.get_state())
    if await state.get_state() in Registration or state is None:
        await msg.answer(text='Заполнените анкету, перед поиском собеседника')
    elif await state.get_state() in Chatting:
        await send_topics(msg)
    # await msg.answer(text='Выбери тему, которую хотите обсудить', reply_markup=kb_topics)


async def info(msg: types.Message):
    res = await database.user2user.get_users_by_topics()
    print(res)
    print(res[0])



def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(topic, commands=['topics'], state='*')
    dp.register_message_handler(anketa, commands=['anketa'], state='*')
    dp.register_message_handler(info, commands=['info'], state='*')
    dp.register_message_handler(stop, commands=['stop'], state='*')