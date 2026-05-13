import random

import vk_api
from TG_bot import detect_intent_texts
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType


def echo(message, user_id, vk_api):
    vk_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1,1000)
    )


def main():
    env = Env()
    env.read_env()
    vk_bot_token = env.str("VK_API_KEY")
    project_id = env.str("PROGECT_ID")
    language_code = "ru"
    vk_session = vk_api.VkApi(token=vk_bot_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            fulfillment_text = detect_intent_texts(project_id, event.user_id, event.text, language_code)
            echo(fulfillment_text, event.user_id, vk)


if __name__ == "__main__":
    main()