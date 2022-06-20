import random

from telegram import InlineKeyboardMarkup
from telegram.ext import (CommandHandler, CallbackQueryHandler, Filters,
                          MessageHandler, Updater)

from dataclasses import dataclass

from adds.consts import (PROCEED, CHECK, START, ZERO, ONE, TWO, FIFTEEN,
                         KEYBOARD_REPLY, TG_TOKEN)
from adds.api_call import get_num, get_api_answer, spare_api


@dataclass
class StatInfo:
    lower = 0
    upper = 3
    reputation = 0
    player_num = 0
    game_level = 0
    url = 'http://numbersapi.com/'
    url_2 = 'https://api.math.tools/numbers/base?number='


def greeting(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=chat.id,
        text=(f'Hi, {name}.\n'
              f'Your level is {StatInfo.game_level}.\n Ready to play a game?'),
        reply_markup=PROCEED
    )

    context.bot.send_photo(chat.id, photo=open('pics/saw.png', 'rb'))


def input_num(update, context):
    chat = update.effective_chat
    guess = update.message['text']
    StatInfo.player_num = guess
    guess = get_num(StatInfo.player_num, StatInfo.url, StatInfo.url_2)
    print(guess)
    StatInfo.player_num = int(guess[ZERO])
    if (int(guess[ZERO]) >= StatInfo.lower) and (
            int(guess[ZERO]) <= StatInfo.upper):
        context.bot.send_message(
            chat_id=chat.id,
            text='Oh, nice. Here is an interesting fact about numbers:'
        )
        try:
            response = get_api_answer(guess[ONE])
            context.bot.send_message(
                chat_id=chat.id,
                text=response['text']
            )

        except ConnectionError:
            context.bot.send_message(
                chat_id=chat.id,
                text=('Here is the converted number to base 2'
                      f' -{spare_api(guess[TWO])}'),
                reply_markup=CHECK
            )

        context.bot.send_message(
            chat_id=chat.id,
            text=("Pal, are you ready to check, "
                  "if you have guessed correctly or not?"
                  "Choose '/check' or '/give up' "),
            reply_markup=InlineKeyboardMarkup(KEYBOARD_REPLY)
        )
    else:
        message = ('Hey pal, enter the number between '
                   f'{StatInfo.lower} and {StatInfo.upper}')
        context.bot.send_message(chat_id=chat.id,
                                 text=message,
                                 reply_markup=PROCEED)


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
    x_num = random.randint(StatInfo.lower, StatInfo.upper)
    if x_num == StatInfo.player_num:
        StatInfo.game_level += ONE
        StatInfo.lower += ONE
        StatInfo.upper += TWO
        StatInfo.reputation += FIFTEEN
        context.bot.send_message(
            chat_id=chat.id,
            text=('Well done!\n Your level is increased!\n'
                  'You gained reputation!'
                  f'Your reputation is {StatInfo.reputation}'
                  'Are you a psychic?\n'
                  'One more time?'),
            reply_markup=START
        )

    elif x_num > StatInfo.player_num:
        context.bot.send_message(
            chat_id=chat.id,
            text=('Wrong! My number is greater.\n'
                  f'My number is  {x_num}.\n One more time?'),
            reply_markup=PROCEED
        )
    elif x_num < StatInfo.player_num:
        context.bot.send_message(
            chat_id=chat.id,
            text=('Wrong! My number is less\n'
                  f'My number is  {x_num}.\n One more time?'),
            reply_markup=PROCEED
        )


def endgame(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=(f'It was a nice game!\n Your level is {StatInfo.game_level}\n'
              f'You gained {StatInfo.reputation} reputation\n'
              "Next time just send me '/start'.\n I'll be waiting."),
        reply_markup=START
    )

    context.bot.send_photo(chat.id, photo=open('pics/saw_2.png', 'rb'))


def main():
    updater = Updater(token=TG_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', greeting))
    updater.dispatcher.add_handler(CommandHandler('proceed', start))
    updater.start_polling()
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & (~ Filters.command), input_num))
    updater.start_polling()
    updater.dispatcher.add_handler(CallbackQueryHandler(
        start_game, pattern='/check'))
    updater.dispatcher.add_handler(CallbackQueryHandler(
        endgame, pattern='/give_up'))
    updater.idle()


if __name__ == '__main__':
    main()
