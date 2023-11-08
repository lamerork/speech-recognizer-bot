from environs import Env
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import detect_intent_texts


def main():
    env = Env()
    env.read_env()

    vk_session = vk.VkApi(token=env.str('VK_TOKEN_GROUP'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer = detect_intent_texts(event.user_id, event.text, 'ru-RU')
            if answer:
                vk_api.messages.send(user_id=event.user_id,
                                     message=answer,
                                     random_id=random.randint(1, 1000))


if __name__ == '__main__':
    main()
