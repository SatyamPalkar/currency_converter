import requests
from datetime import datetime

BASE_URL = "https://api.frankfurter.app"

def get_currency_list():
    try:
        response = requests.get(f"{BASE_URL}/currencies")
        response.raise_for_status()  # Make sure to handle errors if any
        return list(response.json().keys())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching currency list: {e}")
        return []

def get_conversion_rate(currency_from, currency_to):
    """Fetch the latest conversion rate between two currencies."""
    try:
        response = requests.get(f"{BASE_URL}/latest", params={"from": currency_from, "to": currency_to})
        response.raise_for_status()
        data = response.json()
        rate = data["rates"].get(currency_to)
        if rate:
            inverse_rate = 1 / rate
            return rate, inverse_rate
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching conversion rate: {e}")
        return None, None

def get_historical_conversion_rate(currency_from, currency_to, date):
    """Fetch the conversion rate for a specific date."""
    date_str = date.strftime("%Y-%m-%d")  # Ensure date formatting is correct
    try:
        response = requests.get(f"{BASE_URL}/{date_str}", params={"from": currency_from, "to": currency_to})
        response.raise_for_status()
        data = response.json()
        rate = data["rates"].get(currency_to)
        if rate:
            inverse_rate = 1 / rate
            return rate, inverse_rate
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical conversion rate: {e}")
        return None, None
