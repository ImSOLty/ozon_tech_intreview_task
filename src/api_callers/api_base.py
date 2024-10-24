import requests
import enum


class RequestMethod(enum.Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'


class BaseClient:
    def __init__(self, url: str):
        self._url = url

    def __action(self, method: RequestMethod, target_url: str, **kwargs):
        return requests.request(method.value, url=target_url, **kwargs)

    def post(self, target_url: str, **kwargs):
        return self.__action(RequestMethod.POST, target_url, **kwargs)

    def get(self, target_url: str, **kwargs):
        return self.__action(RequestMethod.GET, target_url, **kwargs)

    def delete(self, target_url: str, **kwargs):
        return self.__action(RequestMethod.DELETE, target_url, **kwargs)

    def put(self, target_url: str, **kwargs):
        return self.__action(RequestMethod.PUT, target_url, **kwargs)
