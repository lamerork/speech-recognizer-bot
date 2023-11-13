from environs import Env
import random
import logging
from dotenv import load_dotenv

import telegram
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import detect_intent_texts
from telegram_log import TelegramLogsHandler


logger = logging.getLogger('Logger')


def main():
    env = Env()
    env.read_env()

    load_dotenv()

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
            if not event.to_me:
                continue
            if event.type != VkEventType.MESSAGE_NEW:
                continue

            is_fallback, answer = detect_intent_texts(event.user_id, event.text, 'ru-RU')
            if is_fallback:
                continue

            vk_api.messages.send(
                user_id=event.user_id,
                message=answer,
                random_id=random.randint(1, 1000)
            )

    except ConnectionError:
        logger.warning('Ошибка соединения')

    except Exception as err:
        logger.exception(err)


if __name__ == '__main__':
    main()
