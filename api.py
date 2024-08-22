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

    def get_districts(self):
        return self.get(settings.API_URL + '/districts/')

    def get_categories(self):
        return self.get(settings.API_URL + '/categories/')
