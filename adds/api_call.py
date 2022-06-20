import requests

from adds.consts import URL_2_PARAM


def get_num(num, url, url_2):
    """Получение конечного эндпоинта."""
    url = ''.join([url, num, '?json'])
    url_2 = ''.join([url_2, num, URL_2_PARAM])
    listik = [num, url, url_2]
    return listik


def get_api_answer(url):
    """Получение ответа от API."""
    response = requests.get(url).json()
    return response


def spare_api(url):
    """Получение ответа от резервного API."""
    response = requests.get(url).json()
    text_1 = response['contents']['answer']
    return text_1
