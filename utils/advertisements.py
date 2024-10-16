import os
from typing import Optional

import requests
from pathlib import Path
from settings import BASE_DIR


def create_directory_if_not_exists(directory: str):
    is_directory_exists = os.path.exists(directory)
    if not is_directory_exists:
        os.makedirs(f'{BASE_DIR}/{directory}')


def save_advertisements_photos(
        photos: list[str],
        directory: str
):
    create_directory_if_not_exists(BASE_DIR / directory)

    photos_paths = []

    for photo in photos:
        photo_name = photo.split('/')[-1]
        with open(f'{BASE_DIR}/{directory}/{photo_name}', 'wb') as f:
            photo_bytes = requests.get(photo).content
            f.write(photo_bytes)

        photos_paths.append(f'{directory}/{photo_name}')
        print('photo saved successfully')
    return photos_paths


async def save_photos_from_bot(
        message,
        photos_list
):
    file_names = []
    for photo in photos_list:
        file = await message.bot.get_file(photo)
        file_path = file.file_path
        file_name = file_path.split('/')[-1]
        file_names.append(file_name)
        await message.bot.download_file(file_path, f'photos/{file_name}')
    return file_names