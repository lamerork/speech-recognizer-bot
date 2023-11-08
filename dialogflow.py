from environs import Env
import argparse
import json
import requests

from google.cloud import dialogflow


env = Env()
env.read_env()

project_id = env.str('GOOGLE_PRODJECT_ID')


def detect_intent_texts(session_id, texts, language_code):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if response.query_result.intent.is_fallback:
        return None

    return response.query_result.fulfillment_text


def create_intent(display_name, training_phrases_parts, message_texts):

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

    parser = argparse.ArgumentParser(description='Загрузка json файла с диалогами для DialogFlow')
    parser.add_argument('--json', help='Файл с диалогами')
    parser.add_argument('--link', help='Ссылка на файл с диалогами')
    arguments = parser.parse_args()

    if arguments.json:
        with open(arguments.json, "r") as file:
            training_phrases = json.load(file)

    elif arguments.link:
        response = requests.get(arguments.link)
        response.raise_for_status()

        training_phrases = response.json()
    else:
        print('Параметры не заданы')
        return

    for training_phrase in training_phrases:
        create_intent(training_phrase, 
                      training_phrases[training_phrase]['questions'], 
                      [training_phrases[training_phrase]['answer']])


if __name__ == '__main__':
    main()
