import requests

import consts
from guess_num_bot import StatInfo


def get_num(guess):
    consts.COMPLETE_URL = ''.join([consts.URL, guess, '?json'])
    consts.COMPLETE_URL_2 = ''.join(
        [consts.SECOND_URL, guess, consts.URL_2_PARAM]
    )
    guess = int(guess[0])
    StatInfo.player_num = guess
    return guess


def get_api_answer(url):
    response = requests.get(url).json()
    return response


def spare_api(url):
    response = requests.get(url).json()
    text_1 = response['contents']['answer']
    return text_1
