import requests

from adds.consts import URL_2_PARAM


def get_num(num, url, url_2):
    url = ''.join([url, num, '?json'])
    url_2 = ''.join([url_2, num, URL_2_PARAM])
    listik = [num, url, url_2]
    return listik


def get_api_answer(url):
    response = requests.get(url).json()
    return response


def spare_api(url):
    response = requests.get(url).json()
    text_1 = response['contents']['answer']
    return text_1
