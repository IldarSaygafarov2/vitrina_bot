def realtor_welcome_text(fullname: str):
    return f"Привет, {fullname}!"


def realtor_operation_type_text():
    return "Выберите тип операции: "


def realtor_property_category_text():
    return f"Выберите категорию недвижимости: "


def realtor_selected_property_category_text(property_category: str):
    return f"Выбранная категория недвижимости: <b>{property_category}</b>"


def realtor_photos_quantity_text():
    return "Сколько фотографий добавите для этого объявления?"


def realtor_photos_quantity_get_text():
    return "Отправьте столько фотографий, сколько указали: "


def realtor_title_text():
    return "Напишите заголовок для объявления: "


def realtor_description_text():
    return "Напишите описание для этого объявления: "


def realtor_choose_district_text():
    return "Выберите район, в котором расположена данная недвижимость: "


def realtor_chosen_district_text(district: str):
    return f"Выбранный район: <b>{district}</b>"


def realtor_full_quadrature_of_house():
    return "Укажите общую площадь участка"


def realtor_correct_address_text():
    return "Напишите точный адрес недвижимости"


def realtor_property_type_text():
    return "Выберите тип недвижимости: "


def realtor_property_creation_year_text():
    return "Укажите год постройки новостройки"


def realtor_price_text():
    return "Напишите цену объявления: "


def realtor_is_auction_allowed_text():
    return "Уместен ли торг?"


def realtor_is_property_studio_text():
    return "Квартира является студией?"


def realtor_quadrature_text():
    return ""


def realtor_rooms_from_to_text(is_from: bool):
    if is_from:
        return "Количество комнат от: "
    return "Количество комнат до: "


def realtor_quadrature_from_to_text(is_from: bool):
    if is_from:
        return "Квадратура от: "
    return "Квадратура до: "


def realtor_floor_from_to_text(is_from: bool):
    if is_from:
        return "Этаж от: "
    return "Этаж до: "


def realtor_advertisement_repair_type_text():
    return "Укажите тип ремонта: "


def realtor_advertisement_completed_text(**kwargs):
    rooms_from_to = f'<b>Кол-во комнат</b> от <i>{kwargs["rooms_from"]}</i> до <i>{kwargs["rooms_to"]}</i>'
    creation_year = f'\n<b>Год постройки: </b><i>{kwargs["creation_date"]}</i>' if kwargs["creation_date"] else ''
    house_quadrature = f'\n<b>Общая площадь участка: </b>{kwargs["house_quadrature"]}' if kwargs["house_quadrature"] else ''

    return f"""
<b>Заголовок: </b><i>{kwargs["title"]}</i>
<b>Тип объявления: </b><i>{kwargs["operation_type"]}</i>
<b>Описание: </b><i>{kwargs["description"]}</i>
<b>Район: </b><i>{kwargs["district"]}</i>
<b>Адрес: </b><i>{kwargs["address"]}</i>
<b>Категория недвижимости: </b><i>{kwargs["property_category"]}</i>
<b>Тип недвижимости: </b><i>{kwargs["property_type"]}</i>{creation_year}
<b>Цена: </b><i>{kwargs["price"]}</i>{house_quadrature}
{rooms_from_to if not kwargs["is_studio"] else f'<b>Кол-во комнат: </b> Студия'}
<b>Квадратура: </b>от <i>{kwargs["quadrature_from"]}</i> до <i>{kwargs["quadrature_to"]}</i>
<b>Этаж: </b>от <i>{kwargs["floor_from"]}</i> до <i>{kwargs["floor_to"]}</i>
<b>Ремонт: </b><i>{kwargs["repair_type"]}</i>
"""


def realtor_choose_advertisements_type_text():
    return "Выберите какие объявления показать: "


def realtor_choose_action_below_text():
    return "Выберите действие ниже: "


