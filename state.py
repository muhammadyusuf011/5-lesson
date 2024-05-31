from aiogram.dispatcher.filters.state import State, StatesGroup
class AddUserState(StatesGroup):
    name = State()
    age = State()
    address = State()
    photo = State()


class GetUserState(StatesGroup):
    id = State()


class UpdateUserForm(StatesGroup):
    id = State()
    name = State()
    age = State()
    address = State()
    photo = State()

