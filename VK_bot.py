import random
import os
import logging

import telebot
from telebot import apihelper
import vk_api
from google.cloud import dialogflow
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger(__name__)


class MyLogsHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        # env = Env()
        # env.read_env()
        # proxy_ip = env.str("PROXY")
        # proxy_url = f'socks5h://{proxy_ip}'
        # apihelper.proxy = {'https': proxy_url}
        # chat_id = env.str("TELEGRAM_CHAT_ID")
        # tg_bot_token = env.str("TELEGRAM_BOT_API_KEY")
        # bot_logger = telebot.TeleBot(tg_bot_token)
        # bot_logger.send_message(chat_id=chat_id, text=log_entry)
        print(log_entry)


def detect_intent_texts_and_fallback_flag(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    fulfillment_text = response.query_result.fulfillment_text
    is_fallback = response.query_result.intent.is_fallback
    return fulfillment_text, is_fallback


def echo(message, user_id, vk_api):
    vk_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1,1000)
    )


def main():
    env = Env()
    env.read_env()
    path_key = env.str("PATH_TO_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_key
    vk_bot_token = env.str("VK_API_KEY")
    project_id = env.str("PROGECT_ID")
    language_code = "ru"
    vk_session = vk_api.VkApi(token=vk_bot_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            fulfillment_text, is_fallback = detect_intent_texts_and_fallback_flag(
                                                project_id,
                                                event.user_id,
                                                event.text,
                                                language_code
                                            )
            if not is_fallback:
                echo(fulfillment_text, event.user_id, vk)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    try:
        main()
    except Exception as e:
        logger.error("Бот упал с ошибкой")
        logger.exception(e)
