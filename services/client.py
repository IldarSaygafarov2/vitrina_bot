import requests
from services.api import api_manager

print(api_manager.advertiser_service.get_one(
    advertisement_id=19,
    # data={
    #     'name': 'Vitrina Bot',
    # },
    headers={'Accept-Language': 'uz'}
))
