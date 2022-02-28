from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from config import TOKEN
from config import PORT
import logging
import calendarmessages
import telegramcalendar
import utils
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update:Update, context:CallbackContext):
    update.message.reply_text("Hi ayang {}, hari ini kamu sehat kannn? 😊".format(update.message.from_user.first_name))

def command_help(update:Update, context:CallbackContext):
    update.message.reply_text("Iya sayang, aku pasti ngebantu kamu kok 😊\n/start : Memulai\n/help : Bantuan dari aku\n/calendar : Liyat calendar")

def calendar_handler(update, context):
    update.message.reply_text(text=calendarmessages.calendar_message,
    reply_markup=telegramcalendar.create_calendar())

def inline_handler(update, context):
    query = update.callback_query
    (kind, _, _, _, _) = utils.separate_callback_data(query.data)
    inline_calendar_handler(update, context)

def inline_calendar_handler(update, context):
    selected,date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        context.bot.send_message(chat_id=update.callback_query.from_user.id, 
        text=calendarmessages.calendar_response_message % (date.strftime("%d/%m/%Y")),
        reply_markup=ReplyKeyboardRemove())

if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", command_help))
    dp.add_handler(CommandHandler("calendar", calendar_handler))
    dp.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_webhook("0.0.0.0", PORT, TOKEN, webhook_url='https://tiarabot.herokuapp.com/'+ TOKEN)
    updater.idle()







