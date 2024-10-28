protocol = 'https://'
host = 'otpravka-api.pochta.ru'
path = '/1.0/tariff'

MAX_STANDART_BOX_PARCEL_WEIGTH = 10000

parcel_ordinary = {
    'index-from': '',
    'index-to': '',
    'address-string-from': '',
    'address-string-to': '',
    'mail-category': 'ORDINARY',
    'mail-type': 'POSTAL_PARCEL',
    'mass': 0,
    'dimension': {
        'height': 0,
        'length': 0,
        'width': 0
    },
    'fragile': 'false',
    'transport-type': 'AVIA'
}

parcel_standart = {
    'index-from': '',
    'index-to': '',
    'address-string-from': '',
    'address-string-to': '',
    'mail-category': 'ORDINARY',
    'mail-type': 'POSTAL_PARCEL',
    'mass': 0,
    'dimension-type': '',
    'fragile': 'false',
    'transport-type': 'AVIA'
}