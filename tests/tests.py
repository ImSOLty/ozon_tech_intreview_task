import pytest
import random
import requests
import os
from dotenv import load_dotenv

from src.dogs import get_sub_breeds, u

TOKEN_ENV = "YA_API_TOKEN"


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


def ya_api_token():
    return os.getenv(TOKEN_ENV)


@pytest.mark.parametrize('breed', ['doberman', random.choice(['bulldog', 'collie'])])
def test_proverka_upload_dog(breed):
    token = ya_api_token()
    u(breed, token)
    # проверка
    url_create = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'OAuth {token}'}
    target_url = f'{url_create}?path=/test_folder'
    response = requests.get(target_url, headers=headers)
    assert response.ok, f"Couldn't successfully GET target url ({target_url})"
    assert response.json()['type'] == "dir"
    assert response.json()['name'] == "test_folder"
    assert True
    if get_sub_breeds(breed) == []:
        assert len(response.json()['_embedded']['items']) == 1
        for item in response.json()['_embedded']['items']:
            assert item['type'] == 'file'
            assert item['name'].startswith(breed)

    else:
        assert len(response.json()['_embedded']['items']) == len(get_sub_breeds(breed))
        for item in response.json()['_embedded']['items']:
            assert item['type'] == 'file'
            assert item['name'].startswith(breed)
