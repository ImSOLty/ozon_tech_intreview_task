import pytest
from dotenv import load_dotenv
from uuid import uuid4

from tests.utils import acquire_yandex_cloud_client, acquire_dog_client


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function")
def folder_name():
    # generate unique test folder name
    name = str(uuid4())
    yield name
    # clear folder at the end of the test
    client = acquire_yandex_cloud_client()
    client.remove_folder(name)


@pytest.fixture(scope="session")
def ya_client():
    return acquire_yandex_cloud_client()


@pytest.fixture(scope="session")
def dog_client():
    return acquire_dog_client()
