def realtor_welcome_text(fullname: str):
    return f"Привет, <b>{fullname}</b>"


def choose_one_below_text():
    return "Выберите один из пунктов ниже:"


def total_checked_or_unchecked_advertisements_text(advertisements_list: list, is_checked: bool):
    if is_checked:
        return f'Всего проверенных объявлений: {len(advertisements_list)}'
    return f'Всего непроверенных объявлений: {len(advertisements_list)}'


def choose_category_text(operation_type: str):
    msg = f"""
Выбранный тип операции: <b>{operation_type}</b>

Выберите категорию недвижимости:
"""
    return msg


def chosen_property_category_text(category_name: str):
    return f'Выбранная категория: <b>{category_name}</b>\n\n'


def photos_question_text():
    return "Сколько фотографий добавите для этого объявления?"


def photos_process_number_text(photos_number: int):
    return f'Отправьте {photos_number} фотографий: '