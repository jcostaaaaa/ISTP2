import urllib.parse
from pip._vendor import requests

def get_data_api(home_country):

    address = home_country
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'

    response = requests.get(url).json()

    print(response)

    return[
        response[0]["lat"],
        response[0]["lon"]
    ]


