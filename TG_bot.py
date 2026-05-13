import telebot
from google.cloud import dialogflow
from telebot import types
from environs import Env
from telebot import apihelper


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    fulfillment_text = response.query_result.fulfillment_text
    return fulfillment_text


def main():
    env = Env()
    env.read_env()
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
    	fulfillment_text = detect_intent_texts(project_id, session_id, text, language_code)
    	bot.send_message(message.chat.id, fulfillment_text)
    
    
    bot.infinity_polling()

if __name__ == "__main__":
    main()