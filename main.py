from tools.tools import get_parcel_cost, get_parcel_cost_v2, get_index, get_address


def main():

    destination = {
        'index-from': '101000',
        'index-to': '689251',
        'mail-category': 'ORDINARY',
        'mail-type': 'POSTAL_PARCEL',
        'mass': 3000,
        'dimension': {
            'height': 20,
            'length': 30,
            'width': 50
        },
        'fragile': 'true',
        'declared-value': 8000,
        'transport-type': 'AVIA'
    }

    # cost = get_parcel_cost_v2()
    # print(cost)
    index = '157800'
    # index = get_index(address)
    address = get_address(index)
    print(address)


if __name__ == '__main__':
    main()