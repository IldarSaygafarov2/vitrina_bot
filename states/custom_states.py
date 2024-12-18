from aiogram.fsm.state import State, StatesGroup


class AdvertisementState(StatesGroup):
    operation_type = State()
    property_category = State()
    property_type = State()
    repair_type = State()

    photos = State()
    photos_number = State()

    title = State()
    title_uz = State()

    full_description = State()
    full_description_uz = State()

    district = State()
    district_uz = State()

    address = State()
    address_uz = State()

    price = State()
    auction_allowed = State()

    rooms_from = State()
    rooms_to = State()

    quadrature_from = State()
    quadrature_to = State()

    floor_from = State()
    floor_to = State()

    house_quadrature_from = State()
    house_quadrature_to = State()

    is_studio = State()
    creation_date = State()


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


class AdvertisementUpdatingState(StatesGroup):
    update_name = State()
    update_operation_type = State()
    update_gallery = State()
    update_gallery_photo = State()
    update_description = State()
    update_district = State()
    update_address = State()
    update_property_category = State()
    update_property_type = State()
    update_price = State()
    update_quadrature = State()
    update_creation_date = State()
    update_rooms = State()
    update_floor = State()
    update_repair_type = State()
    update_house_quadrature = State()
    update_is_studio = State()
