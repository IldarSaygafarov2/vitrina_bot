from aiogram.fsm.state import State, StatesGroup


class AdvertisementState(StatesGroup):
    main_categories = State()
    property_categories = State()
    photos = State()
    photos_number = State()
    title = State()
    full_description = State()
    district = State()
    property_type = State()
    price = State()
    rooms_from = State()
    rooms_to = State()
    quadrature_from = State()
    quadrature_to = State()
    floor_from = State()
    floor_to = State()
    repair_type = State()
