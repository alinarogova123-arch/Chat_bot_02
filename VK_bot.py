import random
import os

import vk_api
from google.cloud import dialogflow
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType


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
    path = env.str("GOOGLE_APPLICATION_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
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
    main()