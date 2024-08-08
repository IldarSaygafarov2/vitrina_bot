
from aiogram.fsm.state import State, StatesGroup



class AdvertisementState(StatesGroup):
    photos = State()
    title = State()
