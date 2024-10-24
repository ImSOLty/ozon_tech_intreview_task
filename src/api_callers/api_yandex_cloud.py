from api_callers.api_base import BaseClient
from api_callers.const_api_urls import YA_API_URL

from exceptions import AuthException

RESOURCES_ROUTE = 'resources'
RESOURCES_URLOAD_ROUTE = f'{RESOURCES_ROUTE}/upload'


class YandexCloudClient(BaseClient):
    def __init__(self, token):
        super().__init__(YA_API_URL)
        if token is None:
            raise AuthException(f"{self.__class__.__name__}: No token provided")
        self._request_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {token}'
        }

    def create_new_folder_on_yd(self, path):
        params = {'path': path}
        target_url = f'{self._url}/{RESOURCES_ROUTE}'
        self.put(target_url, headers=self._request_headers, params=params)

    def upload_photos_to_yd(self, path, url_file, name):
        params = {"path": f'/{path}/{name}', 'url': url_file, "overwrite": "true"}
        target_url = f'{self._url}/{RESOURCES_URLOAD_ROUTE}'
        self.post(target_url, headers=self._request_headers, params=params)

    def batch_upload_photos_to_yd(self, path, name_url_dict):
        for name, url in name_url_dict.items():
            self.upload_photos_to_yd(path, url, name)

    def remove_folder(self, path, permanently):
        params = {'path': path, 'permanently': permanently}
        target_url = f'{self._url}/{RESOURCES_ROUTE}'
        self.delete(target_url, headers=self._request_headers, params=params)
