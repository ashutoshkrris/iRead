import requests
from decouple import config


REVUE_BASE_URL = 'https://www.getrevue.co/api'
REVUE_API_KEY = config("REVUE_API_KEY")


def add_subscriber(email: str, first_name: str, last_name: str = None, double_opt_in: bool = False):
    headers = {
        'Authorization': f'Token {REVUE_API_KEY}'
    }
    data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "double_opt_in": double_opt_in
    }
    response = requests.post(
        f"{REVUE_BASE_URL}/v2/subscribers/", json=data, headers=headers)
    return response.status_code == 200


class LocationInformation:

    @staticmethod
    def get_ip():
        response = requests.get('https://api64.ipify.org?format=json').json()
        return response["ip"]

    @staticmethod
    def get_location():
        ip_address = LocationInformation.get_ip()
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        location_data = {
            "ip": ip_address,
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name")
        }
        return location_data
