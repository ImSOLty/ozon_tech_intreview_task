import pytest
import time

from src.uploader import run_uploader

from tests.utils import extract_subbreed_from_filename, parse_file_item, check_operations_completion
from tests.enums import Filetype


@pytest.mark.parametrize('breed', ['doberman', 'affenpinscher'])
def test_upload_dog_breed_without_subs(ya_client, folder_name, breed):
    uploader = run_uploader(folder_name, breed, ya_client._token)

    check_operations_completion(
        condition=uploader.ya_client.check_completed_operations
    )

    response = ya_client.get_folder_content(folder_name)
    assert response.ok, f"Couldn't successfully GET contents of {folder_name}: {response.status_code}"
    file_type, file_name, embedded_items = parse_file_item(response.json())
    assert file_type == Filetype.DIR, \
        f"Expected '{Filetype.DIR}' filetype, found '{file_type}'"
    assert file_name == folder_name, \
        f"Expected '{folder_name}' filename, found '{file_name}'"

    assert len(embedded_items) == 1  # single picture in folder
    for item in embedded_items:
        file_type, file_name, _ = parse_file_item(item)
        assert file_type == Filetype.FILE, \
            f"Expected '{Filetype.FILE}' filetype, found '{file_type}'"
        assert file_name.startswith(breed), \
            f"File name '{file_name}' should start with '{breed}' breed"


@pytest.mark.parametrize('breed', ['bulldog', 'collie'])
def test_upload_dog_breed_with_subs(ya_client, dog_client, folder_name, breed):
    uploader = run_uploader(folder_name, breed, ya_client._token)

    check_operations_completion(
        condition=uploader.ya_client.check_completed_operations
    )

    response = ya_client.get_folder_content(folder_name)
    assert response.ok, f"Couldn't successfully GET contents of {folder_name}: {response.status_code}"
    file_type, file_name, embedded_items = parse_file_item(response.json())
    assert file_type == Filetype.DIR, \
        f"Expected '{Filetype.DIR}' filetype, found '{file_type}'"
    assert file_name == folder_name, \
        f"Expected '{folder_name}' filename, found '{file_name}'"

    sub_breeds_list = set(dog_client.get_sub_breeds_list(breed))
    extracted_sub_breeds = set()

    assert len(embedded_items) == len(sub_breeds_list)
    for item in embedded_items:
        file_type, file_name, _ = parse_file_item(item)
        assert file_type == Filetype.FILE, \
            f"Expected '{Filetype.FILE}' filetype, found '{file_type}'"
        assert file_name.startswith(breed), \
            f"File name '{file_name}' should start with '{breed}' breed"
        extracted_sub_breeds.add(extract_subbreed_from_filename(file_name))

    assert sub_breeds_list == extracted_sub_breeds, \
        f"There is difference between sets of sub breeds: expected {sub_breeds_list}, got {extracted_sub_breeds}"
