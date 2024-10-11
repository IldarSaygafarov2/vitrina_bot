def update_advertisement_name_text(advertisement_name: str):
    return f"""
Текущее название:
<b>{advertisement_name}</b>

Напишите новое название:
"""


def update_operation_type_text(operation_type: str):
    return f"""
Текущий тип операции:
<b>{operation_type}</b>

Выберите новый тип операции ниже:
"""


def update_description_text(description: str):
    return f"""
Текущее описание:
<b><i>{description}</i></b>

Новое описание:
"""


def update_district_text(district_name: str):
    return f"""
Текущий район:
<b><i>{district_name}</i></b>

Новый район:
"""


def update_address_text(address: str):
    return f"""
Текущий адрес:
<b><i>{address}</i></b>

Новый адрес:
"""


def update_price_text(current_price: int):
    return f"""
Текущая цена:
<b><i>{current_price}</i></b>

Новая цена:
"""


def update_repair_type_text(repair_type: str):
    return f"""
Текущее состояние ремонта:
<b><i>{repair_type}</i></b>

Выберите новое:
"""


def update_quadrature_text(quadrature_from: int, quadrature_to: str):
    return f"""
Текущие значения: 
<b><i>Квадратура от: {quadrature_from}</i></b>
<b><i>Квадратура до: {quadrature_to}</i></b>

Укажите новые значения через запятую, важно соблюдать правильный порядок:

<code>40, 50</code>
"""


def update_rooms_text(rooms_from: int, rooms_to: int):
    return f"""
Текущие значения:
<b><i>Кол-во комнат от: {rooms_from}</i></b>
<b><i>Кол-во комнат до: {rooms_to}</i></b>

Укажите новые значения через запятую, важно соблюдать правильный порядок:

<code>3, 5</code> 
"""


def update_floor_text(floor_from: int, floor_to: int):
    return f"""
Текущие значения:
<b><i>Этаж от: {floor_from}</i></b>
<b><i>Этаж до: {floor_to}</i></b>

Укажите новые значения через запятую, важно соблюдать правильный порядок:

<code>3, 5</code> 
"""


def update_creation_date_text(current_creation_date: int):
    return f"""
Текущий год постройки:
<b><i>{current_creation_date}</i></b>

Новый год постройки:
"""


def update_property_category_text(property_category: str):
    return f"""
Текущая категория недвижимости:
<b><i>{property_category}</i></b>

Новая категория недвижимости:
"""


def update_property_type_text(property_type: str):
    return f"""
Текущий тип недвижимости:
<b><i>{property_type}</i></b>

Новый тип недвижимости:
"""