import json
import os
import requests
import pprint
from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    print("Intent created: {}".format(response))


def main():
    env = Env()
    env.read_env()
    path_key = env.str("PATH_TO_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_key

    with open("questions.json", "r", encoding='utf-8') as my_file:
        intents = json.load(my_file)
    
    project_id = env.str("PROGECT_ID")
    for key, value in intents.items():
        display_name = key
        message_texts = [value.get("answer")]
        training_phrases_parts = value.get("questions")
        create_intent(project_id, display_name, training_phrases_parts, message_texts)


if __name__ == "__main__":
    main()
