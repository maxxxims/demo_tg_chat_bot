from aiogram import types
from settings import dp, Messages, bot
from aiogram import Dispatcher
from keyboards import kb_gender, kb_skip
# from aiogram.types import ReplyKeyboardRemove
from FSM import Registration, Chatting
from aiogram.dispatcher import FSMContext
from handlers.topics import send_topics
import database.user, database.user2user




async def set_name(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    async with state.proxy() as data:
        if len(message.text) > 50:
            await message.reply('Слишком длинное имя')
            return None
        data['username'] = message.text
        data['id'] = str(message.from_user.id)
    await Registration.next()
    await message.answer('Укажите свой возраст', reply_markup=kb_skip)


async def set_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit():
            data['age'] = int(message.text)
            await Registration.next()
            await message.answer(text='Укажи свой пол', reply_markup=kb_gender)
        else:
            await message.reply('Некорректный возраст')


async def set_age_callback(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await Registration.next()
    await call.message.answer(text='Укажите свой пол', reply_markup=kb_gender)
    

async def set_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
        await Registration.next()
        await message.reply('Укажите информацию о себе, если хотите')


async def set_gender_callback(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    gender = call.data.split('_')[-1]
    async with state.proxy() as data:
        if gender == 'male' or gender == 'female':
            data['gender'] = gender
            await Registration.next()
            await call.message.answer('Укажите информацию о себе', reply_markup=kb_skip)       
        elif gender == 'skip':
            await Registration.next()
            await call.message.answer('Укажите информацию о себе', reply_markup=kb_skip)
        else:
            await call.answer('Простите, я вас не понял')
    


async def set_bio(message: types.Message, state: FSMContext) -> None:
    if len(message.text) > 500:
        await message.reply('Слишком длинная информация')
        return None
    
    async with state.proxy() as data:
        data['bio'] = message.text
        await database.user.add_user(data)
        await message.reply(text=str(data))
    await state.finish()
    await send_topics(message)


async def set_bio_callback(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text='Анкета заполнена')
    async with state.proxy() as data:
        await database.user.add_user(data)
        await call.message.answer(text=str(data))
        await state.finish()
    await send_topics(call.message)


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(set_name, state=Registration.name)
    dp.register_message_handler(set_age, state=Registration.age)
    # dp.register_message_handler(set_gender, state=Registration.gender)
    dp.register_message_handler(set_bio, state=Registration.bio)
    dp.register_callback_query_handler(set_age_callback, lambda x: x.data == 'skip', state=Registration.age)
    dp.register_callback_query_handler(set_gender_callback, lambda x: x.data.startswith('set_gender'), state=Registration.gender)
    dp.register_callback_query_handler(set_bio_callback, lambda x: x.data == 'skip', state=Registration.bio)
    