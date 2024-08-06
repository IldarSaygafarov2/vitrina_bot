from telebot.handler_backends import State, StatesGroup


class AdState(StatesGroup):
    start_process = State()
    pre_process_photo = State()
    post_process_photo = State()
    title = State()
    description = State()
    district = State()
    estate_type = State()
    price = State()
    rooms_from = State()
    rooms_to = State()
    quadrature_from = State()
    quadrature_to = State()
    floor_from = State()
    floor_to = State()
    repair_type = State()
