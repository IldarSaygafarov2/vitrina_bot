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


def get_categories() -> dict:
    endpoint = settings.API_URL + '/categories/'
    return make_request(endpoint)


class ApiService:
    def get(self, url: str):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def post(self, url: str, data: dict):
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def create_advertisement(self, data: dict) -> dict:
        endpoint = settings.API_URL + '/advertisements/'
        return self.post(endpoint, data)

    def get_districts(self):
        return self.get(settings.API_URL + '/districts/')

    def get_district_id(self, district_slug: str) -> int:
        return self.get(settings.API_URL + '/districts/' + district_slug)

    def get_categories(self):
        return self.get(settings.API_URL + '/categories/')


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