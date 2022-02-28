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
logger = logging.getLogger(__name__)


def start(update:Update, context:CallbackContext):
    update.message.reply_text("Hi ayang {}, hari ini kamu sehat kannn? 😊".format(update.message.from_user.first_name))

def command_help(update:Update, context:CallbackContext):
    update.message.reply_text("Iya sayang, aku pasti ngebantu kamu kok 😊\n/tolong : Aku always siap bantu kamu 🤗\n/kelender : Melihat kalender\n/remind : Ngingetin jadwal kamu 🥰\n/unset : Gk jadi aku ingetin 😔")

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
        context.bot.send_message(chat_id = update.callback_query.from_user.id, 
        text = calendarmessages.calendar_response_message % (date.strftime("%d %B %Y")),
        reply_markup = ReplyKeyboardRemove())

# Alarm
def reminder_word(update:Update, context:CallbackContext):
    update.message.reply_text("Sayang, kalau kamu mau aku ingetin ketik /ingetin <isi waktunya> yaaa 😊")

def set_timer(update: Update, context: CallbackContext):
    """Add a job to the queue."""
    
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text("Sayang, kamu mau ke masa depan?")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, context=chat_id, name=str(chat_id))

        text = "Tenang, nanti aku ingetin ya sayang 😊"
        if job_removed:
            text += "Kamu udah inget duluan yaa hehe"
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text("Contohnya: /ingetin <isi waktunya> sayanggg")

def alarm(context: CallbackContext):
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text="Sayanggg, kamu ngga lupa kan? 🤭")

def unset(update: Update, context: CallbackContext):
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)

def remove_job_if_exists(name: str, context: CallbackContext):
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("tolong", command_help))
    dispatcher.add_handler(CommandHandler("kalender", calendar_handler))
    dispatcher.add_handler(CommandHandler("remind", reminder_word))
    dispatcher.add_handler(CommandHandler("ingetin", set_timer))
    dispatcher.add_handler(CommandHandler("unset", unset))
    
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_webhook("0.0.0.0", PORT, TOKEN, webhook_url='https://tiarabot.herokuapp.com/'+ TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()







