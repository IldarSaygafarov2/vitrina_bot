from aiogram import html


def create_advertisement_message(**kwargs):
    t = f'{html.bold('Кол-во комнат: ')}от {html.italic(kwargs["rooms_from"])} до {html.italic(kwargs["rooms_to"])}'

    return f'''
            {html.bold('Заголовок: ')}
            {html.italic(kwargs['title'])}
            {html.bold('Тип объявления: ')}
            {html.italic(kwargs['main_category'])}
            {html.bold('Описание: ')}
            {html.italic(kwargs['description'])}
            {html.bold('Район: ')}{html.italic(kwargs['district'])}
            {html.bold('Адрес: ')}{html.italic(kwargs['address'])}
            {html.bold('Категория недвижимости: ')}{html.italic(kwargs['property_category'])}
            {html.bold('Тип недвижимости: ')}{html.italic(kwargs['property_type'])}
            {html.bold('Цена: ')}{html.italic(kwargs['price'])}
            {t if not kwargs['is_studio'] else f'{html.bold("Кол-во комнат: ")} Студия'}
            {html.bold('Квадратура: ')}от {html.italic(kwargs['quadrature_from'])} до {html.italic(kwargs['quadrature_to'])}
            {html.bold('Этаж: ')}от {html.italic(kwargs['floor_from'])} до {html.italic(kwargs['floor_to'])}
            {html.bold('Ремонт: ')}{html.italic(kwargs['repair_type'])}
    '''
