import os
import time
from typing import Callable, Any

from src.api_callers.api_yandex_cloud import YandexCloudClient
from src.api_callers.api_dog import DogClient

from tests.enums import Filetype
from tests.consts import TOKEN_ENV


def ya_api_token():
    return os.getenv(TOKEN_ENV)


def acquire_yandex_cloud_client():
    return YandexCloudClient(token=ya_api_token())


def acquire_dog_client():
    return DogClient()


def check_operations_completion(condition: Callable, max_retries: float = 15, timeout: float = 1):
    num_of_retries = 0
    while num_of_retries < max_retries:
        num_of_retries += 1
        if condition():
            return
        time.sleep(timeout)
    raise AssertionError(f"Timeout. YD operations didn't complete in {max_retries} retries")


def parse_file_item(item: dict[str, Any]):
    for field in ['type', 'name']:
        assert field in item, f"There is no '{field}' field in response structure"
    file_type = Filetype(item['type'])
    file_name = item['name']
    file_items = []
    if file_type == Filetype.DIR:
        assert '_embedded' in item, "There is no '_embedded' field in response structure"
        assert 'items' in item['_embedded'], "There is no '_embedded.items' field in response structure"
        file_items = item['_embedded']['items']
    return file_type, file_name, file_items


def extract_subbreed_from_filename(filename: str):
    # according to dog.ceo format is <breed>-<subbreed>
    # where all characters are alphabetic in both of them
    return filename[filename.find('-') + 1:filename.find('_')]
