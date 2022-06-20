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
KEYBOARD_REPLY = [[InlineKeyboardButton("/check", callback_data='HElist8'),
                   InlineKeyboardButton("/give up", callback_data='HRlist8')]]

COMPLETE_URL = ''
COMPLETE_URL_2 = ''
URL_2_PARAM = '8&from=10&to=2'
