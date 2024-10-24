import pytest
import random
import requests

from src.dogs import get_sub_breeds, u


@pytest.mark.parametrize('breed', ['doberman', random.choice(['bulldog', 'collie'])])
def test_proverka_upload_dog(breed):
    u(breed)
    # проверка
    url_create = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'OAuth AgAAAAAJtest_tokenxkUEdew'}
    response = requests.get(f'{url_create}?path=/test_folder', headers=headers)
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
