import imp
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from config import TOKEN
from config import PORT
import logging
import calendarmessages
import telegramcalendar
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update:Update, context:CallbackContext):
    update.message.reply_text("Hi ayang {}, hari ini kamu sehat kannn? 😊".format(update.message.from_user.first_name))

def command_help(update:Update, context:CallbackContext):
    update.message.reply_text("Iya sayang, aku pasti ngebantu kamu kok 😊\n/start : Memulai\n/help : Bantuan dari aku")

def calendar_handler(update, context):
    update.message.reply_text(text=calendarmessages.calendar_message,
    reply_markup=telegramcalendar.create_calendar())


if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", command_help))
    dp.add_handler(CommandHandler("calendar", calendar_handler))

    updater.start_webhook("0.0.0.0", PORT, TOKEN, webhook_url='https://tiarabot.herokuapp.com/'+ TOKEN)
    updater.idle()







