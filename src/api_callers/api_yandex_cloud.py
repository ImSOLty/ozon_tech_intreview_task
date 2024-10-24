from typing import Callable

from src.api_callers.api_base import BaseClient
from src.api_callers.const_api_urls import YA_API_URL
from src.exceptions import AuthException

RESOURCES_ROUTE = 'resources'
RESOURCES_URLOAD_ROUTE = f'{RESOURCES_ROUTE}/upload'


def append_operation(func: Callable):
    def wrapper(*args):
        response = func(*args)
        args[0].awaited_operations.add(response.json()['href'])
        return response
    return wrapper


class YandexCloudClient(BaseClient):

    def __init__(self, token: str):
        super().__init__(YA_API_URL)
        if token is None:
            raise AuthException(f"{self.__class__.__name__}: No token provided")
        self._token = token
        self._request_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {token}'
        }
        self.awaited_operations = set()

    def get_folder_content(self, path: str):
        params = {'path': path}
        target_url = f'{self._url}/{RESOURCES_ROUTE}'
        return self.get(target_url, headers=self._request_headers, params=params)

    @append_operation
    def create_new_folder_on_yd(self, path: str):
        params = {'path': path}
        target_url = f'{self._url}/{RESOURCES_ROUTE}'
        return self.put(target_url, headers=self._request_headers, params=params)

    @append_operation
    def upload_photos_to_yd(self, path: str, url_file: str, name: str):
        params = {"path": f'/{path}/{name}', 'url': url_file, "overwrite": "true"}
        target_url = f'{self._url}/{RESOURCES_URLOAD_ROUTE}'
        return self.post(target_url, headers=self._request_headers, params=params)

    def batch_upload_photos_to_yd(self, path: str, name_url_dict: dict[str, str]):
        for name, url in name_url_dict.items():
            self.upload_photos_to_yd(path, url, name)

    def remove_folder(self, path: str, permanently: bool = True):
        params = {'path': path, 'permanently': permanently}
        target_url = f'{self._url}/{RESOURCES_ROUTE}'
        return self.delete(target_url, headers=self._request_headers, params=params)

    def check_completed_operations(self):
        for operation in list(self.awaited_operations):
            try:
                status = self.get(operation, headers=self._request_headers).json()['status']
                if status != 'in-progress':
                    self.awaited_operations.remove(operation)
            except KeyError:
                self.awaited_operations.remove(operation)
        return not self.awaited_operations
