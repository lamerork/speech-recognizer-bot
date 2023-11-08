from environs import Env
import random
import logging
from time import sleep

import telegram
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

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


def main():
    env = Env()
    env.read_env()

    logger_bot = telegram.Bot(token=env.str('TELEGRAM_LOG_TOKEN'))
    chat_id = env.str('TELEGRAM_CHAT_ID')

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(logger_bot, 'VK Распознование речи', chat_id))

    logger.info('Бот запущен')

    vk_session = vk.VkApi(token=env.str('VK_TOKEN_GROUP'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                answer = detect_intent_texts(event.user_id, event.text, 'ru-RU')
                if answer:
                    vk_api.messages.send(user_id=event.user_id,
                                         message=answer,
                                         random_id=random.randint(1, 1000))

    except ConnectionError:
        logger.warning('Ошибка соединения')
        sleep(60)

    except Exception as err:
        logger.exception(err)


if __name__ == '__main__':
    main()
