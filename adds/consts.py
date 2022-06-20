import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup


load_dotenv()

START = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)
PROCEED = ReplyKeyboardMarkup([['/proceed']], resize_keyboard=True)
CHECK = ReplyKeyboardMarkup([['/check']], resize_keyboard=True)
TG_TOKEN = os.getenv('TOKEN')
URL = 'http://numbersapi.com/'
SECOND_URL = 'https://api.math.tools/numbers/base?number='
KEYBOARD_REPLY = [[InlineKeyboardButton("/check", callback_data='/check'),
                   InlineKeyboardButton("/give up", callback_data='/give_up')]]
KEYBOARD_STATS = [[InlineKeyboardButton("/my_stats", callback_data='/my_stats')]]

ZERO = 0
ONE = 1
TWO = 2
FIFTEEN = 15
URL_2_PARAM = '8&from=10&to=2'
