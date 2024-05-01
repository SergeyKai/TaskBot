from aiogram.fsm.state import State, StatesGroup


class AddTaskStatesGroup(StatesGroup):
    GET_NAME = State()
