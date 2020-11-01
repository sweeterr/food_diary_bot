import os
import logging
from functools import wraps
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
from record import Record
from sheets import update_sheet


PORT = int(os.environ.get('PORT', 5000))
CONFIGS = Config()
# TODO make configs not global


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in CONFIGS.bot["allowed"]:
            logging.info(f"Unauthorized access denied for {user_id}.")
            return
        return func(update, context, *args, **kwargs)
    return wrapped
# TODO add message when access is restricted


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi! This bot can save your meals to Google Sheets. "
                                  "If you want to test this bot, contact @no_sweeterr. \n\n"
                                  "/start - Description and list of commands.\n"
                                  "/add - Add a food diary record. E.g.: scrambled eggs on toast. "
                                  "You can specify time and/or date separated by semicolon: "
                                  "25.10.2020; 13:00; soup, tea. If you don't do this, "
                                  "current time and date will be added.")


@restricted
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


def error(update, context):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater = Updater(token=CONFIGS.bot["token"], use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=CONFIGS.bot["token"])
    updater.bot.setWebhook('https://food-diary-bot.herokuapp.com/' + CONFIGS.bot["token"])
    updater.idle()


if __name__ == "__main__":
    main()
