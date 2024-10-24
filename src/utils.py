from src.exceptions import InvalidBreedUrlException


def extract_filename_from_url(url: str):
    part_name = url.split('/')
    if len(part_name) < 2:
        raise InvalidBreedUrlException
    name = f'{part_name[-2]}_{part_name[-1]}'
    return name
