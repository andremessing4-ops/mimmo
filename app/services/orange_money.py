import requests

def create_orange_payment(amount, phone):

    url = "https://api.orange.com/payment"  # remplacer par vraie API

    data = {
        "amount": amount,
        "phone": phone
    }

    response = requests.post(url, json=data)

    return response.json()