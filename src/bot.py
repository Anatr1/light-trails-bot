#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import os
from uuid import uuid4
from secret import TOKEN
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, Bot, InlineQueryResultCachedPhoto
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

#TOKEN = 'INSERT_HERE_YOUR_TELEGRAM_BOT_TOKEN'
c_id = -1001341349922

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
bot = Bot(TOKEN)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def inlinequery(update: Update, context: CallbackContext) -> None:
	"""Handle the inline query."""
	query = update.inline_query.query

	magic_word = query.split()[0] #PERICOLOSO, INPUT NON SANITIZZATI
	os.system('./shadow_long '+magic_word)
	os.system('convert '+magic_word+".pgm -rotate 90 "+magic_word+"_R.pgm")

	infophoto = bot.sendPhoto(chat_id=c_id, photo=open("./"+magic_word+"_R.pgm",'rb'),caption=magic_word)
	thumbphoto = infophoto["photo"][0]["file_id"]
	originalphoto = infophoto["photo"][-1]["file_id"]

	results = [
		InlineQueryResultCachedPhoto(
			id=uuid4(),
			title="CachedPhoto",
			photo_file_id=originalphoto, caption=magic_word)
	]
	
	update.inline_query.answer(results)


def main() -> None:
    #Remove previous pics
    os.system('rm *.pgm')

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()