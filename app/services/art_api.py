import requests

BASE_URL = "https://api.artic.edu/api/v1/artworks"


def get_artwork(external_id: int):

    response = requests.get(f"{BASE_URL}/{external_id}")

    if response.status_code != 200:
        return None

    data = response.json()

    if "data" not in data:
        return None

    return data["data"]


def artwork_exists(external_id: int) -> bool:

    return get_artwork(external_id) is not None


def get_artwork_title(external_id: int):

    artwork = get_artwork(external_id)

    if artwork is None:
        return None

    return artwork.get("title")