import requests
from geopy import Nominatim
from geopy.exc import GeopyError

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}


def get_city_from_coordinates(latitude, longitude):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json",
            "addressdetails": 1,
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(response)
        print(data)
        location_info = data.get("address", {}).get("city")
        print("Location Info: {}".format(location_info))
        return location_info
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_city_by_coordinates(latitude, longitude) -> str:
    geolocator = Nominatim(user_agent="location_bot")
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        return location.__str__()
    except GeopyError as e:
        print(f"Geocoding error: {e}")
        return "Не распознано"
