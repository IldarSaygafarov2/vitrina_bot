from aiogram import html


def create_advertisement_message(**kwargs):
    t = f'{html.bold('Кол-во комнат: ')}от {html.italic(kwargs["rooms_from"])} до {html.italic(kwargs["rooms_to"])}'
    msg = f"""
<b>Заголовок: </b>
<i>{kwargs['title']}</i>
<b>Тип объявления: </b>
<i>{kwargs['main_category']}</i>
<b>Описание: </b>
<i>{kwargs['description']}</i>
<b>Район: </b><i>{kwargs['district']}</i>
<b>Адрес: </b><i>{kwargs['address']}</i>
<b>Категория недвижимости: </b><i>{kwargs['property_category']}</i>
<b>Тип недвижимости: </b><i>{kwargs['property_type']}</i>
<b>Цена: </b><i>{kwargs['price']}</i>
{t if not kwargs['is_studio'] else f'<b>Кол-во комнат: </b> Студия'}
<b>Квадратура: </b>от <i>{kwargs['quadrature_from']}<i> до <i>{kwargs['quadrature_to']}</i>
<b>Квадратура: </b>от <i>{kwargs['floor_from']}<i> до <i>{kwargs['floor_to']}</i>
<b>Ремонт: </b><i>{kwargs['repair_type']}</i>
    """
    return msg
