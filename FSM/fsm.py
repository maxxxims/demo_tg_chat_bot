from aiogram.dispatcher.filters.state import State, StatesGroup

class Registration(StatesGroup):
    name = State()
    age = State()
    gender = State()
    bio = State() 



class Chatting(StatesGroup):
    searching = State()
    ongoing = State()