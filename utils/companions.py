from FSM.fsm import Chatting
import database.user2user, database.user
from aiogram.types import Message
from logic.anketa import make_anketa
from settings import bot


async def find_companion(id: str, topic: str) -> bool:
    companion = await database.user2user.find_companion(id, topic)
    if len(companion) == 0:
        # await bot.send_message(int(id), text=f'Идёт поиск собеседника')
        return False
    else:
        await database.user2user.set_companion(id, topic, str(companion[0]))
        companion_info = await database.user.get_user(str(companion[0]))
        user_info = await database.user.get_user(id)
        companions_anketa = make_anketa(companion_info)
        users_anketa = make_anketa(user_info)
        await bot.send_message(id,
            text=f'собеседник найден.\nТема: {topic}\n{companions_anketa}')


        await Chatting.ongoing.set()
        await bot.send_message(companion_info.id,
            text=f'собеседник найден.\nТема: {topic}\n{users_anketa}')
        return True