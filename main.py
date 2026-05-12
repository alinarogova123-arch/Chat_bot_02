import telebot
from telebot import types
from environs import Env

env = Env()
env.read_env()
tg_bot_token = env.str("TELEGRAM_BOT_API_KEY")
bot = telebot.TeleBot(tg_bot_token)

@bot.message_handler(commands=["start","help"])
def handle_start(message):
	bot.send_message(message.chat.id, "Здравствуйте")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
	bot.send_message(message.chat.id, message.text)

bot.infinity_polling()