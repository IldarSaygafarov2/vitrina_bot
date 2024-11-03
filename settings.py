import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

API_URL = os.getenv('API_URL')
WEB_APP_URL = os.getenv('WEB_APP_URL')

BASE_DIR = Path(__file__).resolve().parent
KB_FIELDS = [
    ('update_name', 'Название'),
    ('update_operation_type', 'Тип операции'),
    ('update_gallery', 'Фотки'),
    ('update_description', 'Описание'),
    ('update_district', 'Район'),
    ('update_address', 'Адрес'),
    ('update_property_category', 'Категория недвижимости'),
    ('update_property_type', 'Тип недвижимости'),
    ('update_price', 'Цена'),
    ('update_quadrature', 'Квадратура'),
    ('update_creation_date', 'Дата постройки'),
    ('update_rooms', 'Кол-во комнат'),
    ('update_floor', 'Этаж'),
    ('update_repair_type', 'Тип ремонта'),
    ('update_house_quadrature', 'Площадь дома'),
    ('update_is_studio', 'Студия'),
]
KB_FIELDS = {item[0]: item[1] for item in KB_FIELDS}

OPERATION_TYPES = {
    'rent': 'Аренда',
    'buy': 'Покупка'
}

OPERATION_TYPES_UZ = {
    'rent': 'Ijara',
    'buy': 'Sotib olish'
}

ADVERTISEMENT_RANGE_FIELDS = {
    'quadrature_from': 'Квадратура от',
    'quadrature_to': 'Квадратура до',
    'rooms_qty_from': 'Кол-во комнат от',
    'rooms_qty_to': 'Кол-во комнат до',
    'floor_from': 'Этаж от',
    'floor_to': 'Этаж до'
}

REPAIR_TYPES = {
    "with": "С ремонтом",
    "without": "Без ремонта",
    "designed": "Дизайнерский ремонт",
    "rough": "Черновая",
    "pre_finished": "Предчистовая",
}

REPAIR_TYPES_UZ = {
    "С ремонтом": ("Yangilangan", 'with'),
    "Без ремонта": ("Ta'mirsiz", 'without'),
    "Дизайнерский ремонт": ("Dizayner ta'mirlash", 'designed'),
    "Черновая": ("Qoralama", 'rough'),
    "Предчистовая": ("Oldindan tugatish", 'pre_finished'),
}

REPAIR_TYPES_REVERSED = {value: key for key, value in REPAIR_TYPES.items()}

PROPERTY_TYPES = {
    'new': 'Новостройка',
    'old': 'Вторичный фонд'
}
PROPERTY_TYPES_REVERSED = {value: key for key, value in PROPERTY_TYPES.items()}

PROPERTY_TYPES_UZ = {
    'Новостройка': ('Yangi bino', 'new'),
    'Вторичный фонд': ('Ikkilamchi fond', 'old')
}
