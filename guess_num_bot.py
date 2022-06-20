import random

from telegram import InlineKeyboardMarkup
from telegram.ext import (CommandHandler, Filters,
                          MessageHandler, Updater)

import consts
from api_call import get_num, get_api_answer, spare_api


class StatInfo:
    lower = 0
    upper = 3
    x_num = random.randint(lower, upper)
    player_num = 0
    game_level = 0


def greeting(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = consts.PROCEED
    context.bot.send_message(
        chat_id=chat.id,
        text=(f'Hi, {name}.\n'
              f'Your level is {StatInfo.game_level}.\n Ready to play a game?'),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, photo=open('pics/saw.png', 'rb'))


def input_num(update, context):
    chat = update.effective_chat
    guess = update.message['text']
    try:
        guess = get_num(guess)
        if (guess >= StatInfo.lower) and (
                guess <= StatInfo.upper):
            context.bot.send_message(
                chat_id=chat.id,
                text='Oh, nice. Here is an interesting fact about numbers:'
            )
            try:
                response = get_api_answer(consts.COMPLETE_URL)
                context.bot.send_message(
                    chat_id=chat.id,
                    text=response['text']
                )

            except ConnectionError:
                context.bot.send_message(
                    chat_id=chat.id,
                    text=('Here is the converted number to base 2'
                          f' -{spare_api(consts.COMPLETE_URL_2)}'),
                    reply_markup=consts.CHECK
                )
            #context.bot.send_message(
             #   chat_id=chat.id,
              #  text=response['text']
           # )
            context.bot.send_message(
                chat_id=chat.id,
                text=("Pal, are you ready to check, "
                      "if you have guessed correctly or not?"
                      "Choose '/check' or '/give up' "),
                reply_markup=InlineKeyboardMarkup(consts.KEYBOARD_REPLY)
            )
            return guess
        else:
            message = ('Hey pal, enter the number between '
                       f'{StatInfo.lower} and {StatInfo.upper}')
            context.bot.send_message(chat_id=chat.id,
                                     text=message,
                                     reply_markup=consts.PROCEED)

    except ValueError:
        message = 'Pal, the number is to be positive integer! '
        context.bot.send_message(chat_id=chat.id,
                                 text=message,
                                 reply_markup=consts.PROCEED)


def start(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=("You've got only one try.\n Good luck!\n"
              f'Enter the num between {StatInfo.lower} and {StatInfo.upper}: ')
    )
    return context


def start_game(update, context):
    chat = update.effective_chat
    user_num = StatInfo.player_num
    if StatInfo.x_num == user_num:
        StatInfo.game_level += 1
        StatInfo.lower += 1
        StatInfo.upper += 2
        context.bot.send_message(
            chat_id=chat.id,
            text=(f'Well done! Your level is increased! Are you a psychic?\n'
                  'One more time?'),
            reply_markup=consts.START
        )

    elif StatInfo.x_num > user_num:
        context.bot.send_message(
            chat_id=chat.id,
            text=('Wrong! My num is greater.\n'
                  f'My number is  {StatInfo.x_num}.\n One more time?'),
            reply_markup=consts.PROCEED
        )
    elif StatInfo.x_num < user_num:
        context.bot.send_message(
            chat_id=chat.id,
            text=('Wrong! My num is less\n'
                  f'My number is  {StatInfo.x_num}.\n One more time?'),
            reply_markup=consts.PROCEED
        )


def main():
    updater = Updater(token=consts.TG_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', greeting))
    updater.dispatcher.add_handler(CommandHandler('proceed', start))
    updater.start_polling()
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & (~ Filters.command), input_num))
    updater.start_polling()
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text('/check'), start_game))
    updater.idle()


if __name__ == '__main__':
    main()
