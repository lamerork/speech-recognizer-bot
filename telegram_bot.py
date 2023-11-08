from environs import Env
import logging
from time import sleep
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow import detect_intent_texts


logger = logging.getLogger('Logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, bot_name, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot
        self.bot_name = bot_name

    def emit(self, record):
        log_entry = f'<b>{self.bot_name}:</b>\n{self.format(record)}'
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry, parse_mode=telegram.ParseMode.HTML)


def start(update: telegram.Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте!')


def reply(update: telegram.Update, context: CallbackContext) -> None:
    session_id = update.effective_user['id']
    answer = detect_intent_texts(session_id, update.message.text, 'ru-RU')
    if answer == None:
        answer = 'Попробуй, пожалуйста, выразить свою мысль по-другому'
    update.message.reply_text(answer)


def main():
    env = Env()
    env.read_env()

    updater = Updater(env.str('TELEGRAM_TOKEN'))
    logger_bot = telegram.Bot(token=env.str('TELEGRAM_LOG_TOKEN'))
    chat_id = env.str('TELEGRAM_CHAT_ID')

    dispatcher = updater.dispatcher

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(logger_bot, 'ТГ Распознование речи', chat_id))

    logger.info('Бот запущен')

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    try:
        updater.start_polling()
        updater.idle()

    except ConnectionError:
        logger.warning('Ошибка соединения')
        sleep(60)

    except Exception as err:
        logger.exception(err)


if __name__ == '__main__':
    main()
