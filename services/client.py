import requests
from services.api import api_manager

print(api_manager.advertiser_service.get_one(advertisement_id=1, headers={'Accept-Language': 'uz'}))



