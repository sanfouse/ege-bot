from aiogram.dispatcher.filters.state import State, StatesGroup

class CheckNumbers(StatesGroup):
    
    menu = State()
    check_answer = State()
