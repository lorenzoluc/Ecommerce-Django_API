import requests

BASE_URL = "http://127.0.0.1:8000/api"


def get_products():
    url = f"{BASE_URL}/products/"

    response = requests.get(url)
    print(response.text)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.json())
        return None