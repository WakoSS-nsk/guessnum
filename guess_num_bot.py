import os

import guess_game
import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()

TG_TOKEN = os.getenv('TOKEN')
NASA_KEY = os.getenv('NASA_TOKEN')
URL = f'https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}&count=1'


def get_new_image():
    response = get_url()
    return response[0]


def get_url():
    response = requests.get(URL)
    response = response.json()
    random_pic = response[0].get('hdurl')
    description = response[0].get('explanation')
    list_objects = [random_pic, description]
    return list_objects


def get_description():
    response = get_url()
    return response[1]


def new_pic(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())
    context.bot.send_message(chat.id, get_description())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/space_photo']], resize_keyboard=True)
    get_url()

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Насладись бесконечным космосом'.format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_image())
    context.bot.send_message(chat.id, get_description())


def main():
    updater = Updater(token=TG_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, new_pic))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
