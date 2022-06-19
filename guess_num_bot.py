import os
import random


import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import (CommandHandler, Filters,
                          MessageHandler, Updater)

load_dotenv()

START = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)
PROCEED = ReplyKeyboardMarkup([['/proceed']], resize_keyboard=True)
TG_TOKEN = os.getenv('TOKEN')
URL = 'http://numbersapi.com/'
SECOND_URL = 'https://api.math.tools/numbers/base?number='


class StatInfo:
    lower = 0
    upper = 3
    x_num = random.randint(lower, upper)
    player_num = 0
    game_level = 0


def greeting(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = PROCEED
    context.bot.send_message(
        chat_id=chat.id,
        text=(f'Hi, {name}.\n'
              f'Your level is {StatInfo.game_level}.\n Ready to play a game?'),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, photo=open('pics/saw.png', 'rb'))


def input_num(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/check']], resize_keyboard=True)
    try:
        guess = update.message['text']
        num_fact = ''.join([URL, guess, '?json'])
        guess = int(guess[0])
        StatInfo.player_num = guess
        if guess >= StatInfo.lower or guess <= StatInfo.upper:
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
                    text=f'Here is the converted number to base 2 -{text_1}',
                    reply_markup=button
                )

            context.bot.send_message(
                chat_id=chat.id,
                text=response['text'],
                reply_markup=button
            )
            return StatInfo.player_num
        else:
            raise InputError(
                f'Дружок, введи число от {StatInfo.lower} до {StatInfo.upper}')
    except ValueError:
        raise ValueError('Дружок, введи целое положительное число: ')


def start(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=("You've got only one try.\n Good luck!\n"
              f'Enter the num between {StatInfo.lower} and {StatInfo.upper}:- ')
    )
    return context


def start_game(update, context):
    chat = update.effective_chat
    user_num = StatInfo.player_num
    if StatInfo.x_num == user_num:
        StatInfo.game_level += 1
        StatInfo.lower += 1
        StatInfo.upper += 2
        button = START
        context.bot.send_message(
            chat_id=chat.id,
            text=(f'Well done! Your level is increased! Are you a psychic?\n'
                  'One more time?'),
            reply_markup=button
        )

    elif StatInfo.x_num > user_num:
        button = PROCEED
        context.bot.send_message(
            chat_id=chat.id,
            text=('Wrong! My num is greater.\n'
                  f'My number is  {StatInfo.x_num}.\n One more time?'),
            reply_markup=button
        )
    elif StatInfo.x_num < user_num:
        button = PROCEED
        context.bot.send_message(
            chat_id=chat.id,
            text=('Wrong! My num is less\n'
                  f'My number is  {StatInfo.x_num}.\n One more time?'),
            reply_markup=button
        )


def main():
    buttons = ['/check']
    markup = ReplyKeyboardMarkup.from_column(buttons)
    updater = Updater(token=TG_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', greeting))
    updater.dispatcher.add_handler(CommandHandler('proceed', start))
    updater.start_polling()
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & (~ Filters.command), input_num))
    updater.start_polling()
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text(buttons[0]), start_game))
    updater.idle()


if __name__ == '__main__':
    main()
