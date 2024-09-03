def get_repair_type_by_name(repair_type_name):
    repair_types = {
        'С ремонтом': 'with',
        'Без ремонта': 'without',
        'Дизайнерский ремонт': 'designed',
        'Черновая': 'rough',
        'Предчистовая': 'pre_finished'
    }
    return repair_types[repair_type_name]
