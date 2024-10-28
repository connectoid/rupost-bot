import requests
import base64
import json
import os
from pprint import pprint
from datetime import datetime
import urllib


from dotenv import load_dotenv

from settings.settings import protocol, host, path

def to_base64(str):
    return base64.b64encode(str.encode()).decode('utf-8')

load_dotenv()

LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
login_password = to_base64(f'{LOGIN}:{PASSWORD}')

sizes = {
    '10': 'S - до 260х170х80 мм',
    '20': 'M - до 300х200х150 мм',
    '30': 'L - до 400х270х180 мм',
    '40': 'XL - 530х260х220 мм',
}

request_headers = {
    'Content-Type': 'Application/json',
    'Accept': 'application/json;charset=UTF-8',
    'Authorization': 'AccessToken ' + ACCESS_TOKEN,
    'X-User-Authorization': 'Basic ' + login_password
}


def get_parcel_cost(parcel):

    url = protocol + host + path

    response = requests.post(
        url,
        headers=request_headers,
        data=json.dumps(parcel)
    )
    # cost = response.json()['total-rate']
    # print(f'Status code: {response.status_code}')
    print(f'Response body: {response}')

    return response


def get_parcel_cost_v2(parcel):
    from_index = parcel['index-from']
    return_index = parcel['index-from']
    to_index = parcel['index-to']
    weight = parcel['mass']
    date = datetime.today().date().strftime("%Y%m%d")
    time = datetime.now().strftime("%H%M")
    if 'dimension-type' in parcel:
        object = '27030'
        pack = parcel['dimension-type']
        url = f'https://tariff.pochta.ru/v2/calculate/tariff?json&object={object}&from={from_index}&to={to_index}&weight={weight}&pack={pack}&return={return_index}&date={date}&time={time}'
        text_size = sizes[pack]
        size = f'Коробка размера {text_size}'
    else:
        object = '4030'
        width = parcel['dimension']['width']
        height = parcel['dimension']['height']
        length = parcel['dimension']['length']
        url = f'https://tariff.pochta.ru/v2/calculate/tariff?json&object={object}&from={from_index}&to={to_index}&return={return_index}&weight={weight}&size={width}x{height}x{length}&date={date}&time={time}'
        size = f'{width} cм x {height} cм x {length} cм'
    response = requests.get(url)
    # print(f'Response body: {response.text}')
    pprint(response.json())
    total = int(response.json()['paymoneynds']) / 100
    sum = int(response.json()['paymoney']) / 100
    nds = int(response.json()['nds']) / 100
    address_string_from = parcel['address-string-from']
    address_string_to = parcel['address-string-to']
    answer = (f'Адрес отправителя: {from_index}, {address_string_from}\n'
        f'<b>Адрес получателя:</b> {to_index}, {address_string_to}\n'
        f'<b>Размер:</b> {size}\n'
        f'<b>Вес:</b> {float(weight)/1000} кг\n'
        f'<b>Сумма без НДС:</b> {sum} руб.\n'
        f'<b>НДС 20%:</b> {nds} руб.\n'
        f'<b>Итого сумма с НДС 20%:</b> {total} руб.\n\n'
        f'<i>(Перешлите это сообщение себе в Избранное, чтобы не потерять информацию при продолжении диалога)</i> ')

    return answer


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
    if 'postoffices' in response.json():
          return response.json()['postoffices'][0]
    else:
          print(f'Индекс по запросу {address} не найден')
          return None
    

def get_address(index):
    protocol 	= "https://"
    host 		= "otpravka-api.pochta.ru"

    postalCode 	= ""

    request_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "Authorization": "AccessToken " + ACCESS_TOKEN,
        "X-User-Authorization": "Basic " + login_password
    }

    path = "/postoffice/1.0/" + index

    url = protocol + host + path

    response = requests.get(url, headers=request_headers)
    if response.status_code != 200:
        print(f'Адрес по индексу {index} не найден')
        return None
    else:
        address_json = response.json()
        region = address_json['region'] + ', '
        settlement = address_json['settlement'] + ', '
        if 'district' in address_json:
            district = address_json['district'] + ', '
        else:
            district = ''
        address_source = address_json['address-source']
        address = f'{region}{settlement}{district}{address_source}'
        return address


def index_check(text: str) -> str:
    address_string = ''
    if all(ch.isdigit() for ch in text) and 100000 <= int(text) <= 800000:
        address = get_address(text)
        if address:
            address_string = address
            return f'{text}*{address_string}'
    elif not all(ch.isdigit() for ch in text):
        address_string = text
        index = get_index(text)
        if index:
            return f'{index}*{address_string}'
    raise ValueError


def weight_check(text: str) -> str:
    if all(ch.isdigit() for ch in text) and 1 <= int(text) <= 50000:
        return text
    raise ValueError


def weight_standart_box_check(text: str) -> str:
    if all(ch.isdigit() for ch in text) and 1 <= int(text) <= 10000:
        return text
    raise ValueError


def size_check(text: str) -> str:
    if all(ch.isdigit() for ch in text) and 1 <= int(text) <= 200:
        return text
    raise ValueError