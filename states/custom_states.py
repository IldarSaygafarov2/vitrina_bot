from aiogram.fsm.state import State, StatesGroup


class AdvertisementState(StatesGroup):
    operation_type = State()
    property_category = State()

    photos = State()
    photos_number = State()
    title = State()
    full_description = State()
    district = State()
    address = State()
    property_type = State()
    price = State()
    auction_allowed = State()
    rooms_from = State()
    rooms_to = State()
    quadrature_from = State()
    quadrature_to = State()
    floor_from = State()
    floor_to = State()
    repair_type = State()
    is_studio = State()
    creation_date = State()
    house_quadrature = State()


class RGProcessState(StatesGroup):
    show_moderated = State()
    realtor_data = State()
    process_adverts = State()
    process_checked = State()
    process_unchecked = State()


class AdvertisementEditingState(StatesGroup):
    start = State()
    process = State()
    check = State()