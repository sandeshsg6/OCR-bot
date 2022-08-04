import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image
import pytesseract
import os
import constants

#from traceback import print_exc

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(constants.welcome_text)

def reply_for_text_message (update, context):
    update.message.reply_text(constants.reply_to_text_message)

def convert_image (update, context):
    file_name = "test.jpg"
    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    newFile.download(file_name)
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
    update.message.reply_text("Your image is under processing! \n\n ")
    # print(pytesseract.get_languages(config=''))
    extracted_text = pytesseract.image_to_string(Image.open(file_name))
    update.message.reply_text(extracted_text)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    bot_token = os.environ.get("BOT_TOKEN","")
    updater = Updater(bot_token, use_context=True) 

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_for_text_message))

    #on sending an image
    dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, convert_image))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
