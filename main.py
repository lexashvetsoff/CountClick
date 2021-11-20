import os
import requests
from urllib.parse import urlparse
import argparse
from dotenv import load_dotenv

load_dotenv()

BITLY_TOKEN = os.getenv('TOKEN')


def shorten_link(token, long_url):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'

    payload = {
        "long_url": long_url
    }

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()['link']


def get_parsed_link(url):
    link = urlparse(url)
    return f'{link.netloc}{link.path}'


def count_clicks(token, bitlink):
    parsed_link = get_parsed_link(bitlink)
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_link}/clicks/summary'

    payload = {
        'unit': 'day',
        'units': -1
    }

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, params=payload, headers=headers)
    response.raise_for_status()

    return response.json()['total_clicks']


def is_bitlink(url, token):
    parsed_link = get_parsed_link(url)
    get_url = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_link}'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(get_url, headers=headers)

    return response.ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_url')
    args = parser.parse_args()
    user_url = args.user_url

    if is_bitlink(user_url, BITLY_TOKEN):
        print(count_clicks(BITLY_TOKEN, user_url))
    else:
        try:
            bitlink = shorten_link(BITLY_TOKEN, user_url)
            print('Битлинк', bitlink)
        except requests.exceptions.HTTPError:
            print('Ошибка запроса!')


if __name__ == '__main__':
    main()
