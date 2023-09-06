from aiogram import types
from settings import dp, Messages, bot
from aiogram import Dispatcher
from keyboards import kb_gender, kb_skip, kb_topics
# from aiogram.types import ReplyKeyboardRemove
from FSM import Chatting
from aiogram.dispatcher import FSMContext
# from aiogram.types import CallbackQuery
import schemas  
import database.user2user, database.user
from utils.anketa import make_anketa
from utils.companions import find_companion


async def send_topics(msg: types.Message):
    await msg.answer(text='Выбери тему, которую хотите обсудить', reply_markup=kb_topics)
    await Chatting.searching.set()


async def set_topic(call: types.CallbackQuery, state: FSMContext):
    topic = call.data.split('_')[-1]
    print(topic)
    user = await database.user2user.get_user_info(str(call.from_user.id))
    # print('*'*10, call.message.from_user.id, call.from_user.id, user)
    if user is None:
        print('user nun')
        await database.user2user.insert_user_in_expectation(str(call.from_user.id), topic)
    else:
        print('user yes')
        await database.user2user.update_user_in_expectation(str(call.from_user.id), topic)
    result = await find_companion(str(call.from_user.id), topic)
    if not result:
        await call.message.answer(text='Идёт поиск собеседника...')
    # some logic to find user
    # companion = await database.user2user.find_companion(str(call.from_user.id), topic)
    # if len(companion) == 0:
    #     await call.message.answer(text=f'Идёт поиск собеседника')
    # else:
    #     await database.user2user.set_companion(str(call.from_user.id), topic, str(companion[0].id))
    #     companion_info = await database.user.get_user(str(companion[0].id))
    #     user_info = await database.user.get_user(str(call.from_user.id))
    #     companions_anketa = make_anketa(companion_info)
    #     users_anketa = make_anketa(user_info)
    #     await call.message.answer(
    #         text=f'собеседник найден.\nТема: {topic}\n{companions_anketa}')


    #     await Chatting.ongoing.set()
    #     await bot.send_message(companion_info.id,
    #         text=f'собеседник найден.\nТема: {topic}\n{users_anketa}')



def register_handlers_topics(dp: Dispatcher):
    dp.register_callback_query_handler(set_topic, lambda x: x.data.startswith('set_topic'), state=Chatting.searching)
