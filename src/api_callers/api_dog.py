from src.api_callers.api_base import BaseClient
from src.api_callers.const_api_urls import DOG_API_URL

from src.exceptions import BreedNotFoundException

BREED_ROUTE = 'breed'
SUB_BREEDS_ROUTE = f'{BREED_ROUTE}/{{breed}}'
RANDOM_IMAGE_ROUTE = f'{SUB_BREEDS_ROUTE}/images/random'
LIST_ROUTE = f'{SUB_BREEDS_ROUTE}/list'


class DogClient(BaseClient):
    def __init__(self):
        super().__init__(DOG_API_URL)

    def get_sub_breeds_list(self, breed):
        target_url = f'{self._url}/{LIST_ROUTE}'.format(breed=breed)
        return self.get(target_url).json().get('message', [])

    def __get_random_image_url(self, breed, sub_breed=None):
        breed = breed if sub_breed is None else f'{breed}/{sub_breed}'
        target_url = f'{self._url}/{RANDOM_IMAGE_ROUTE}'.format(breed=breed)
        response = self.get(target_url)
        if not response.ok:
            raise BreedNotFoundException(f"Not found: {breed}{('/' + sub_breed) if sub_breed else ''}")
        return response.json().get('message')

    def get_images_of_breed(self, breed):
        sub_breeds = self.get_sub_breeds_list(breed)
        if len(sub_breeds):
            return [self.__get_random_image_url(breed, sub_breed) for sub_breed in sub_breeds]
        return [self.__get_random_image_url(breed)]
