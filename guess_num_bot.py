import os
import random
import math

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import (CommandHandler, Filters,
                          MessageHandler, Updater)

load_dotenv()

TG_TOKEN = os.getenv('TOKEN')
URL = 'http://numbersapi.com/'
LOWER = 0
UPPER = 10
LEVEL = LOWER
X_NUM = random.randint(LOWER, UPPER)
GUESS_QUANTITY = round(math.log(UPPER - LOWER + 1, 2))


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


def new_pic(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def greeting(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/proceed!']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Готов сыграть со мной в игру?'.format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, photo=open('pics/saw.png', 'rb'))


def input_num(update, context):
    chat = update.effective_chat
    try:
        guess = update.message['text']
        num_fact = ''.join([URL, guess, '?json'])
        #num_fact = 'http://numbersapi.com/5?json'
        guess = int(guess[0])
        if guess >= LOWER or guess <= UPPER:
            context.bot.send_message(
                chat_id=chat.id,
                text='Oh, nice. Here is an interesting fact about this number:'
            )
            response = requests.get(num_fact).json()
            print(response)
            context.bot.send_message(
                chat_id=chat.id, text=response['text'])
            return guess
        raise InputError(
            f'Дружок, введи число от {LOWER} до {UPPER}'
        )
    except ValueError:
        raise ValueError('Дружок, введи целое положительное число: ')
    return guess


def start(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id, text=f'Угадай число от {LOWER} до {UPPER}:- '
                              f'Количество попыток: {GUESS_QUANTITY}. Удачи!'
    )
    return context


def start_game(update, context):
    chat = update.effective_chat
    tries_count = 0
    while tries_count < GUESS_QUANTITY:
        tries_count += 1
        user_num = input_num()
        if X_NUM == user_num:
            print(f'Молодец! C {tries_count} попыток')
            break
        elif X_NUM > user_num:
            print('Не угадал! Моё число больше.')
        elif X_NUM < user_num:
            print('Не угадал! Моё число меньше.')
    if tries_count >= GUESS_QUANTITY:
        print(f'Я загадал {X_NUM}')
        print('Повезет в другой раз!')


def main():
    updater = Updater(token=TG_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', greeting))
    updater.dispatcher.add_handler(CommandHandler('proceed', start))
    updater.start_polling()
    updater.dispatcher.add_handler(MessageHandler(Filters.text, input_num))
    updater.start_polling()
    updater.dispatcher.add_handler(MessageHandler(Filters.text, input_num))
    updater.idle()


if __name__ == '__main__':
    main()
