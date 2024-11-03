import requests

import settings


class ApiService:
    @staticmethod
    def get(url: str, **kwargs):
        response = requests.get(url, **kwargs)
        # response.raise_for_status()
        return response.json()

    @staticmethod
    def post(url: str, **kwargs):
        response = requests.post(url, **kwargs)
        return response.json()

    @staticmethod
    def patch(url: str, data, **kwargs):
        response = requests.patch(url, data, **kwargs)
        response.raise_for_status()
        return response.json()


class CategoryAPIService(ApiService):
    def get_categories(self) -> list:
        return self.get(settings.API_URL + '/categories/')

    def get_category(self, category_slug: str, **kwargs) -> dict:
        return self.get(settings.API_URL + '/categories/' + category_slug, **kwargs)


class DistrictAPIService(ApiService):
    def get_districts(self):
        return self.get(settings.API_URL + '/districts/')

    def get_district(self, district_slug: str, **kwargs) -> int:
        return self.get(settings.API_URL + '/districts/' + district_slug, **kwargs)


class AdvertisementGalleryAPIService(ApiService):
    def get_advertisement_gallery(self, advertisement_id: int, **kwargs):
        endpoint = f'{settings.API_URL}/advertisements/{advertisement_id}/gallery/'
        return self.get(endpoint, **kwargs)

    def upload_image_to_gallery(self, advertisement_id: int, **kwargs):
        endpoint = f'{settings.API_URL}/advertisements/{advertisement_id}/gallery/'
        return self.post(endpoint, **kwargs)

    def update_image_gallery(self, advertisement_id: int, gallery_id: int, **kwargs):
        endpoint = f'{settings.API_URL}/advertisements/{advertisement_id}/gallery/{gallery_id}/'
        return self.patch(endpoint, **kwargs)


class AdvertisementAPIService(ApiService):
    ADVERTISEMENTS_BASE_URL: str = settings.API_URL + '/advertisements/'
    ADVERTISEMENTS_DEEP_URL: str = settings.API_URL + '/advertisements/{kwarg}/'

    def create_advertisement(self, **kwargs):
        return self.post(self.ADVERTISEMENTS_BASE_URL, **kwargs)

    def get_all(self, **kwargs):
        return self.get(self.ADVERTISEMENTS_BASE_URL, **kwargs)

    def get_one(self, advertisement_id: int, **kwargs):
        endpoint = self.ADVERTISEMENTS_DEEP_URL.format(kwarg=advertisement_id)
        return self.get(endpoint, **kwargs)

    def update_advertisement(self, advertisement_id: int, data, **kwargs):
        endpoint = self.ADVERTISEMENTS_DEEP_URL.format(kwarg=advertisement_id)
        return self.patch(endpoint, data, **kwargs)


class UserAPIService(ApiService):
    def get_user_id(self, tg_username: str) -> int:
        return self.get(settings.API_URL + '/users/' + tg_username + '/user/')

    def get_user_type(self, tg_username: str) -> bool:
        endpoint = f'{settings.API_URL}/users/{tg_username}/type'
        return self.get(endpoint)

    def get_all_users(self, **kwargs):
        endpoint = f'{settings.API_URL}/users/'
        return self.get(endpoint, **kwargs)

    def get_user_advertisements(self, user_id: int, **kwargs) -> list:
        endpoint = f'{settings.API_URL}/users/{user_id}/advertisements/'
        return self.get(endpoint, **kwargs)

    def update_user_tg_user_id(self, user_id: int, data, **kwargs):
        endpoint = f'{settings.API_URL}/users/{user_id}/'
        return self.patch(endpoint, data, **kwargs)

    def get_user(self, user_id: int, **kwargs):
        endpoint = f'{settings.API_URL}/users/{user_id}'
        return self.get(endpoint, **kwargs)


class AdvertisementModerationAPIService(ApiService):
    def get_realtor_advertisements_for_moderation(self, realtor_id: int, **kwargs) -> list:
        url = f'{settings.API_URL}/users/{realtor_id}/moderation_advertisements/'
        return self.get(url, **kwargs)

    def update_moderation_rejection_reason(
            self, realtor_id: int, moderation_id: int, data, **kwargs
    ) -> dict:
        url = f'{settings.API_URL}/users/{realtor_id}/moderation_advertisements/{moderation_id}/'
        return self.patch(url, data, **kwargs)


class UserTypeService(ApiService):
    def get_all_users_by_user_type(self, user_type: str, **kwargs) -> list:
        endpoint = f'{settings.API_URL}/users/'
        return self.get(endpoint, params={'user_type': user_type}, **kwargs)


class APIManager(ApiService):
    def __init__(self):
        self.category_service: CategoryAPIService = CategoryAPIService()
        self.district_service: DistrictAPIService = DistrictAPIService()
        self.advertiser_service: AdvertisementAPIService = AdvertisementAPIService()
        self.user_service: UserAPIService = UserAPIService()
        self.moderation: AdvertisementModerationAPIService = AdvertisementModerationAPIService()
        self.gallery: AdvertisementGalleryAPIService = AdvertisementGalleryAPIService()
        self.user_type: UserTypeService = UserTypeService()


api_manager = APIManager()

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
