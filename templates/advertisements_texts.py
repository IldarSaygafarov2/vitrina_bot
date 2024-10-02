def choose_one_below_text():
    return "Выберите один из пунктов ниже: "


def total_checked_or_unchecked_advertisements_text(advertisements_list: list, is_checked: bool):
    if is_checked:
        return f'Всего проверенных объявлений: {len(advertisements_list)}'
    return f'Всего непроверенных объявлений: {len(advertisements_list)}'


def choose_category_text():
    return 'Выберите категорию для недвижимости: '