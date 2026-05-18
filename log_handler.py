import logging

import telebot
from environs import Env
from telebot import apihelper


class MyLogsHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        env = Env()
        env.read_env()
        proxy_ip = env.str("PROXY")
        proxy_url = f'socks5h://{proxy_ip}'
        apihelper.proxy = {'https': proxy_url}
        tg_bot_token = env.str("TELEGRAM_BOT_API_KEY")
        self.chat_id = env.str("TELEGRAM_CHAT_ID")
        self.bot_logger = telebot.TeleBot(tg_bot_token)


    def emit(self, record):
        log_entry = self.format(record)
        self.bot_logger.send_message(chat_id=self.chat_id, text=log_entry)

