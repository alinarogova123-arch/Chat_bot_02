import json
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
	display_name = "Устройство на работу"
	url_for_get_phrases = env.str("URL_PHRASES")
	response = requests.get(url_for_get_phrases)
	response.raise_for_status()
	intent_data = response.json().get(display_name)

	project_id = env.str("PROGECT_ID")
	training_phrases_parts = intent_data.get("questions")
	message_texts = [intent_data.get("answer")]
	create_intent(project_id, display_name, training_phrases_parts, message_texts)


if __name__ == "__main__":
	main()
