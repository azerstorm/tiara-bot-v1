from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from config import TOKEN, PORT
import logging, calendarmessages, telegramcalendar, utils, converstion as R

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update:Update, context:CallbackContext):
    update.message.reply_text("Ayanggg {}, hari ini kamu sehat kannn? 😊".format(update.message.from_user.first_name))

def command_help(update:Update, context:CallbackContext):
    update.message.reply_text("Iya sayang, aku pasti ngebantu kamu kok 😊\n/kelender : Melihat kalender\n/remind : Ngingetin jadwal kamu 🥰\n/unset : Gk jadi aku ingetin 😔")

#Calendar
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

#Coversation
GENDER, PHOTO, LOCATION, BIO = range(4)

def confess(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Gay', 'Gay']]

    update.message.reply_text(
        'Send /cancel to stop talking to me.\n\n'
        'Are you a Gay or a Gay?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Gay or Gay?'
        ),
    )

    return GENDER

def gender(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Aku udah liat, Coba kirim photo kamu, '
        'Jadi aku tau wujud kamu seperti apa hehe, atau send /skip kalau kamu tidak mau',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO

def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'Naysee, coba kirim lokasi kamu atau /skip kalau kamu gk mau'
    )

    return LOCATION

def skip_photo(update: Update, context: CallbackContext) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'I bet you look great! Now, send me your location please, or send /skip.'
    )

    return LOCATION

def location(update: Update, context: CallbackContext) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    update.message.reply_text(
        'Maybe I can visit you sometime! At last, tell me something about yourself.'
    )

    return BIO

def skip_location(update: Update, context: CallbackContext) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        'Kamu introvert yaa, Coba tulis sesuatu tentang diri kamu.'
    )

    return BIO

def bio(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Makasih, aku harap kita bisa chatting lagi suatu saat')

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Makasih, aku harap kita bisa chatting lagi suatu saat', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

#Conversation
def handle_message(updata:Update, context:CallbackContext):
    text = str(updata.message.text).lower()

    response = R.sample_response(text)

    updata.message.reply_text(response)

def error(update:Update, context:CallbackContext):
    print(f"Update {update} caused error {context.error}")


#Main Program
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("sayang", start))
    dispatcher.add_handler(CommandHandler("tolong", command_help))
    dispatcher.add_handler(CommandHandler("kalender", calendar_handler))
    dispatcher.add_handler(CommandHandler("remind", reminder_word))
    dispatcher.add_handler(CommandHandler("ingetin", set_timer))
    dispatcher.add_handler(CommandHandler("unset", unset))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    dispatcher.add_error_handler(error)
    
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("confess", confess)],
        states={
            GENDER: [MessageHandler(Filters.regex('^(Gay|Gay)$'), gender)],
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler("skip", skip_photo)],
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler("skip", skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    dispatcher.add_handler(conv_handler)

    # Kabar
   
    # Start the Bot
    updater.start_webhook("0.0.0.0", PORT, TOKEN, webhook_url='https://tiarabot.herokuapp.com/'+ TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()







