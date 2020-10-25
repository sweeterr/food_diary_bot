import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
from record import Record
from sheets import update_sheet


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi! I can save your meals to Google Sheets.")


def add(update, context):
    if context.args:
        inputs = " ".join(context.args)
        logging.info(f"Received input: {inputs}.")
        record = Record(inputs, "food")
        update_sheet(record, test=False)
        message = f"I've added the following record to the food diary:\n{record.message}"
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Empty record! Please write what you want to add.")


def main():
    configs = Config()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater = Updater(token=configs.bot["token"], use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add))
    updater.start_polling()


if __name__ == "__main__":
    main()
