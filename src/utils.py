def extract_filename_from_url(url):
    part_name = url.split('/')
    if len(part_name) < 2:
        return None
    name = f'{part_name[-2]}_{part_name[-1]}'
    return name
