from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from config import TOKEN

def start(update:Update, context:CallbackContext):
    update.message.reply_text("Hi ayang {}".format(update.message.from_user.username))

if __name__ == '__main__':
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()
