from environs import Env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow import detect_intent_texts


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте!')


def reply(update: Update, context: CallbackContext) -> None:
    session_id = update.effective_user['id']
    answer = detect_intent_texts(session_id, update.message.text, 'ru-RU')
    if answer == None:
        answer = 'Попробуй, пожалуйста, выразить свою мысль по-другому'
    update.message.reply_text(answer)


def main():
    env = Env()
    env.read_env()

    updater = Updater(env.str('TELEGRAM_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
