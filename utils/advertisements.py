import os

import requests

from settings import BASE_DIR


def create_directory_if_not_exists(directory: str):
    is_directory_exists = os.path.exists(directory)
    if not is_directory_exists:
        os.makedirs(f'{BASE_DIR}/{directory}')


def save_advertisements_photos(
        photos: list[str],
        directory: str
):
    create_directory_if_not_exists(directory)

    for photo in photos:
        photo_name = photo.split('/')[-1]
        with open(f'{directory}/{photo_name}', 'wb') as f:
            photo_bytes = requests.get(photo).content
            f.write(photo_bytes)
        print('photo saved successfully')