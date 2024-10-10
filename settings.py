import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')

API_URL = 'http://127.0.0.1:8000/api/v1'

BASE_DIR = Path(__file__).resolve().parent
KB_FIELDS = [
    ('title', 'Название'),
    ('operation_type', 'Тип операции'),
    ('description', 'Описание'),
    ('district', 'Район'),
    ('address', 'Адрес'),
    ('property_category', 'Категория недвижимости'),
    ('property_type', 'Тип недвижимости'),
    ('price', 'Цена'),
    ('quadrature_from', 'Квадратура от'),
    ('quadrature_to', 'Квадратура до'),
    ('creation_date', 'Дата постройки'),
    ('rooms_from', 'Кол-во комнат от'),
    ('rooms_to', 'Кол-во комнат до'),
    ('floor_from', 'Этаж от'),
    ('floor_to', 'Этаж до'),
    ('repair_type', 'Тип ремонта'),
    ('house_quadrature', 'Площадь дома'),
    ('is_studio', 'Студия'),
]