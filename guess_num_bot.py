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
SECOND_URL = 'https://api.math.tools/numbers/base?number='
LOWER = 0
UPPER = 10
LEVEL = LOWER
X_NUM = random.randint(LOWER, UPPER)
GUESS_QUANTITY = round(math.log(UPPER - LOWER + 1, 2))


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
    print(update.message)
    try:
        guess = update.message['text']
        num_fact = ''.join([URL, guess, '?json'])
        guess = int(guess[0])
        if guess >= LOWER or guess <= UPPER:
            context.bot.send_message(
                chat_id=chat.id,
                text='Oh, nice. Here is an interesting fact about numbers:'
            )
            try:
                response = requests.get(num_fact).json()
            except ConnectionError:
                raise ConnectionError('API недоступен')
                param = '8&from=10&to=2'
                new_url = ''.join([SECOND_URL, guess, param])
                response = requests.get(new_url).json()
                text_1 = new_url['contents']['answer']
                context.bot.send_message(
                    chat_id=chat.id,
                    text=f'Here is the converted number to base 2 -{text_1}')
            context.bot.send_message(
                chat_id=chat.id,
                text=response['text'],
                reply_markup=button
            )
        else:
            raise InputError('Дружок, введи число от {LOWER} до {UPPER}')
    except ValueError:
        raise ValueError('Дружок, введи целое положительное число: ')


def start(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['check']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=(f'Количество попыток: {GUESS_QUANTITY}. Удачи!'
              f'Введи число от {LOWER} до {UPPER}:- и нажми check'),
        reply_markup=button
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
    buttons = ['check', 'next_step']
    markup = ReplyKeyboardMarkup.from_column(buttons)
    updater = Updater(token=TG_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', greeting))
    updater.dispatcher.add_handler(CommandHandler('proceed', start))
    updater.start_polling()
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text(buttons[0]), input_num))
    updater.start_polling()
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text(buttons[1]), start_game))
    updater.idle()


if __name__ == '__main__':
    main()
