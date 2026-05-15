import os
import logging

import telebot
from log_handler import MyLogsHandler
from google_dialogflow_api import detect_intent_texts_and_fallback_flag
from environs import Env
from telebot import apihelper


logger = logging.getLogger(__name__)


def main():
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    env = Env()
    env.read_env()
    path_key = env.str("PATH_TO_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_key
    proxy_ip = env.str("PROXY")
    proxy_url = f'socks5h://{proxy_ip}'
    apihelper.proxy = {'https': proxy_url}
    tg_bot_token = env.str("TELEGRAM_BOT_API_KEY")
    project_id = env.str("PROGECT_ID")
    language_code = "ru"
    bot = telebot.TeleBot(tg_bot_token)
    
    
    @bot.message_handler(commands=["start","help"])
    def handle_start(message):
        bot.send_message(message.chat.id, "Здравствуйте")
    
    
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        text = message.text
        session_id = message.from_user.id
        fulfillment_text, is_fallback = detect_intent_texts_and_fallback_flag(
                                            project_id,
                                            session_id,
                                            text,
                                            language_code
                                        )
        bot.send_message(message.chat.id, fulfillment_text)
    
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error("Бот упал с ошибкой")
        logger.exception(e)


if __name__ == "__main__":
    main()

