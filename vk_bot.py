import random
import os
import logging

from log_handler import MyLogsHandler
import vk_api
from google_dialogflow_api import detect_intent_texts_and_fallback_flag
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger(__name__)


def send_message_to_vk_chat(message, user_id, vk_api):
    vk_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1,1000)
    )


def main():
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    env = Env()
    env.read_env()
    path_key = env.str("PATH_TO_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_key
    vk_bot_token = env.str("VK_API_KEY")
    project_id = env.str("PROGECT_ID")
    language_code = "ru"
    vk_session = vk_api.VkApi(token=vk_bot_token)
    vk = vk_session.get_api()
    try:
        longpoll = VkLongPoll(vk_session)
    except Exception as e:
        logger.error("Бот упал с ошибкой")
        logger.exception(e)
    for event in longpoll.listen():
        if event.type != VkEventType.MESSAGE_NEW or not event.to_me:
            continue
        session_id = f"vk-{event.user_id}"
        text = event.text
        fulfillment_text, is_fallback = detect_intent_texts_and_fallback_flag(
                                            project_id,
                                            session_id,
                                            text,
                                            language_code
                                        )
        if is_fallback:
            continue
        send_message_to_vk_chat(fulfillment_text, event.user_id, vk)


if __name__ == "__main__":
    main()

