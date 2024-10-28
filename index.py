# -*- coding: utf-8 -*-

import requests
import base64
import json
import urllib
import os

from dotenv import load_dotenv

load_dotenv()

def to_base64(str):
	return base64.b64encode(str.encode()).decode("utf-8")

LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
login_password = to_base64(f'{LOGIN}:{PASSWORD}')

# address = "Ярославль Силикатное шоссе 17"

def get_index(address):

    protocol 	= "https://"
    host 		= "otpravka-api.pochta.ru"

    request_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "Authorization": "AccessToken " + ACCESS_TOKEN,
        "X-User-Authorization": "Basic " + login_password
    }

    path = "/postoffice/1.0/by-address?address=" + urllib.parse.quote_plus(address) + "&top=30"

    url = protocol + host + path

    response = requests.get(url, headers=request_headers)
    print("Status code: ", response.status_code)
    print("Response body: ", response.text)
    if response.json()['postoffices']:
          return response.json()['postoffices'][0]
    else:
          print('Индекс по запросу {address} не найден')
          return None


def get_address(index):
    protocol 	= "https://"
    host 		= "otpravka-api.pochta.ru"

    postalCode 	= "689251"

    request_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "Authorization": "AccessToken " + ACCESS_TOKEN,
        "X-User-Authorization": "Basic " + login_password
    }

    path = "/postoffice/1.0/" + postalCode

    url = protocol + host + path

    response = requests.get(url, headers=request_headers)
    print("Status code: ", response.status_code)
    print("Response body: ", response.text)