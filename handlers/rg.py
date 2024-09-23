from aiogram import types, Router, F, html
from aiogram.filters import CommandStart

from keyboards import reply, callback

from services.api import api_manager
from services.user import user_manager

router = Router(name='rg_user')


@router.message(CommandStart(), F.func(lambda msg: user_manager.is_user_rg(msg.from_user.username)))
async def rg_start(message: types.Message):
    await message.answer(f'Привет, Руководитель группы', reply_markup=reply.rg_start_kb())


@router.message(F.text == 'Список риелторов')
async def rg_realtors(message: types.Message):
    res = api_manager.user_service.get_all_users(params={'user_type': 'group_director'})
    await message.answer('Список риелторов', reply_markup=callback.realtors_kb(res))


@router.callback_query(F.data.contains('realtor'))
async def rg_realtors_ads(callback_query: types.CallbackQuery):
    _, realtor_username, user_id = callback_query.data.split('-')
    objects: list[dict] = api_manager.user_service.get_user_advertisements(user_id=int(user_id))
    await callback_query.message.answer(f'Все объявления риелтора: {html.bold(realtor_username)}')
    for obj in objects:
        print(obj)

        t = f'{html.bold('Кол-во комнат: ')}от {html.italic(obj.get('rooms_qty_from'))} до {html.italic(obj.get('rooms_qty_to'))}'
        t2 = f'\n{html.bold("Год постройки: ")}{html.italic(obj.get('creation_year'))}' if obj.get('creation_year') else ''
        #
        msg = f'''
{html.bold('Заголовок: ')}
{html.italic(obj.get('name'))}
{html.bold('Тип объявления: ')}
{html.italic(obj.get('operation_type'))}
{html.bold('Описание: ')}
{html.italic(obj.get('description'))}
{html.bold('Район: ')}{html.italic(obj.get('district').get('name'))}
{html.bold('Адрес: ')}{html.italic(obj.get('address'))}
{html.bold('Категория недвижимости: ')}{html.italic(obj.get('category').get('name'))}
{html.bold('Тип недвижимости: ')}{html.italic(obj.get('property_type'))}{t2}
{html.bold('Цена: ')}{html.italic(obj.get('price'))}
{t if not obj.get('is_studio') else f'{html.bold("Кол-во комнат: ")} Студия'}
{html.bold('Квадратура: ')}от {html.italic(obj.get('quadrature_from'))} до {html.italic(obj.get('quadrature_to'))}
{html.bold('Этаж: ')}от {html.italic(obj.get('floor_from'))} до {html.italic(obj.get('floor_to'))}
{html.bold('Ремонт: ')}{html.italic(obj.get('repair_type'))}
'''
        # await callback_query.message.answer(msg)
        photos = []
        for idx, photo in enumerate(obj.get('gallery')):
            photo_obj = types.InputMediaPhoto(media=photo['photo'])
            photos.append(photo_obj)

        await callback_query.message.answer_media_group(photos)

        #
        # await callback_query.message.answer_media_group(media)
