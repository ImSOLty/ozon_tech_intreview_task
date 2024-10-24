from argparse import ArgumentParser

from src.api_callers.api_yandex_cloud import YandexCloudClient
from src.api_callers.api_dog import DogClient
from src.utils import extract_filename_from_url


class Uploader():
    def __init__(self, ya_token):
        self.ya_client = YandexCloudClient(token=ya_token)
        self.dog_client = DogClient()

    # main action
    def upload_breed(self, folder_path, breed):
        self.ya_client.create_new_folder_on_yd(folder_path)
        breed_urls = self.dog_client.get_images_of_breed(breed)
        name_url_dict = {}
        for breed_url in breed_urls:
            name = extract_filename_from_url(breed_url)
            name_url_dict[name] = breed_url
        self.ya_client.batch_upload_photos_to_yd(folder_path, name_url_dict)


def run_uploader(folder_path, breed, token):
    uploader = Uploader(token)
    uploader.upload_breed(folder_path, breed)
    return uploader


if __name__ == '__main__':
    parser = ArgumentParser()
    for arg in ['folder_path', 'breed', 'token']:
        parser.add_argument(arg)
    args = parser.parse_args()
    run_uploader(args.folder_path, args.breed, args.token)
