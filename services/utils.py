import os
from typing import Optional

import requests
from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.callback import return_back_kb

from services.api import api_manager
from settings import BASE_DIR


def get_repair_type_by_name(repair_type_name):
    repair_types = {
        'С ремонтом': 'with',
        'Без ремонта': 'without',
        'Дизайнерский ремонт': 'designed',
        'Черновая': 'rough',
        'Предчистовая': 'pre_finished'
    }
    return repair_types[repair_type_name]


def get_property_type(property_name):
    property_types = {
        'Новостройка': 'new',
        'Вторичный фонд': 'old'
    }
    return property_types[property_name]


def create_advertisement_message(item: dict) -> str:
    name = item.get('name')
    description = item.get('description')
    operation_type = item.get('operation_type')
    rooms_qty_from = item.get('rooms_qty_from')
    rooms_qty_to = item.get('rooms_qty_to')
    creation_year = item.get('creation_year')
    district = item.get('district')
    address = item.get('address')
    category = item.get('category')
    property_type = item.get('property_type')
    price = item.get('price')
    is_studio = item.get('is_studio')
    quadrature_from = item.get('quadrature_from')
    quadrature_to = item.get('quadrature_to')
    floor_from = item.get('floor_from')
    floor_to = item.get('floor_to')
    repair_type = item.get('repair_type')

    t = f'{html.bold('Кол-во комнат: ')}от {html.italic(rooms_qty_from)
                                            } до {html.italic(rooms_qty_to)}'
    t2 = f'\n{html.bold("Год постройки: ")}{html.italic(
        creation_year)}' if creation_year else ''
    #
    return f'''
{html.bold('Заголовок: ')}
{html.italic(name)}
{html.bold('Тип объявления: ')}
{html.italic(operation_type)}
{html.bold('Описание: ')}
{html.italic(description)}
{html.bold('Район: ')}{html.italic(district.get('name'))}
{html.bold('Адрес: ')}{html.italic(address)}
{html.bold('Категория недвижимости: ')}{html.italic(category.get('name'))}
{html.bold('Тип недвижимости: ')}{html.italic(property_type)}{t2}
{html.bold('Цена: ')}{html.italic(price)}
{t if not is_studio else f'{html.bold("Кол-во комнат: ")} Студия'}
{html.bold('Квадратура: ')}от {html.italic(quadrature_from)} до {html.italic(quadrature_to)}
{html.bold('Этаж: ')}от {html.italic(floor_from)} до {html.italic(floor_to)}
{html.bold('Ремонт: ')}{html.italic(repair_type)}
'''


def download_medias_from_api(path: str, media_url: str):
    media_folder_exists = os.path.exists(os.path.join(BASE_DIR, 'media'))
    if not media_folder_exists:
        os.makedirs(os.path.join(BASE_DIR, 'media'))
    filename = path.split('/')[-1]
    with open(f'media/{filename}', 'wb') as f:
        f.write(requests.get(media_url).content)


async def update_advertisement_text_field(
        message: Message,
        state: FSMContext,
        state_field_name: str,
        updating_field_name: Optional[str] = None,
        addon_fields: Optional[dict[str, int]] = None
):
    new_value = message.text

    current_state = await state.get_data()
    advertisement_id = current_state.get('advertisement_id')
    current_msg: Message = current_state.get(state_field_name)

    if updating_field_name:
        data = {updating_field_name: new_value}
    else:
        data = addon_fields

    api_manager.advertiser_service.update_advertisement(
        advertisement_id=advertisement_id,
        data=data
    )

    await current_msg.edit_text(
        text=f'Успешно обновлено\n\n'
        f'Новое значение: <b>{new_value}</b>',
        reply_markup=return_back_kb(f'advertisement_update:{advertisement_id}')
    )
    current_state.pop(state_field_name)
    await message.delete()
