from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from config import TOKEN
from config import PORT
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update:Update, context:CallbackContext):

    update.message.reply_text("Hi ayang {}, hari ini kamu sehat kannn? 😊".format(update.message.from_user.first_name))


if __name__ == '__main__':
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    updater.start_webhook("0.0.0.0", PORT, TOKEN, webhook_url='https://tiarabot.herokuapp.com/'+ TOKEN)
    updater.idle()



def findat(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i

def send_findig(update:Update, message):
    update.message.reply_text(message, '(placeholder text)')

def send_help(update:Update, message):
    update.message.reply_text(message, 'ALPHA = FEATURES MAY NOT WORK')

dp.add_handler(CommandHandler("findig", send_findig))
dp.add_handler(CommandHandler("help", send_help))


