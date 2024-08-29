import requests
import settings


def make_request(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def is_user_realtor(tg_username: str) -> bool:
    endpoint = settings.API_URL + '/users/' + tg_username + '/type/'
    data = make_request(endpoint)
    return data['user_type'] == 'realtor'


class ApiService:
    def get(self, url: str):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def post(self, url: str, **kwargs):
        response = requests.post(url, **kwargs)
        return response.json()


class CategoryAPIService(ApiService):
    def get_categories(self) -> list:
        return self.get(settings.API_URL + '/categories/')

    def get_category(self, category_slug: str) -> dict:
        return self.get(settings.API_URL + '/categories/' + category_slug)


class DistrictAPIService(ApiService):
    def get_districts(self):
        return self.get(settings.API_URL + '/districts/')

    def get_district(self, district_slug: str) -> int:
        return self.get(settings.API_URL + '/districts/' + district_slug)


class AdvertisementAPIService(ApiService):
    def create_advertisement(self, **kwargs):

        return self.post(settings.API_URL + '/advertisements/', **kwargs)


class APIManager(ApiService):
    def __init__(self):
        self.category_service: CategoryAPIService = CategoryAPIService()
        self.district_service: DistrictAPIService = DistrictAPIService()
        self.advertiser_service: AdvertisementAPIService = AdvertisementAPIService()


"""
{
    "name": "",
    "description": "",
    "district": 1,
    "price": null,
    "rooms_qty_from": null,
    "rooms_qty_to": null,
    "quadrature_from": null,
    "quadrature_to": null,
    "floor_from": null,
    "floor_to": null,
    "auction_allowed": false,
    "category": 1,
    "gallery": []
}
"""
