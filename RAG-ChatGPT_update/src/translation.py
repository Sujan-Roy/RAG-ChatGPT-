import requests, uuid
from dotenv import load_dotenv
import os

load_dotenv()

Azure_key = os.getenv('KEY')
Azure_endpoint = os.getenv('ENDPOINT')
class Translator:
    """
    A class for translating text using Azure's Text Translation API.

    Attributes:
        None

    Methods: """
def trans():
# Add your key and endpoint
    key= Azure_key
    endpoint = Azure_endpoint

    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
    location = "CanadaCentral"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': 'ja'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Read input text from a file
    file_path = "results/"
    with open(file_path +"summary.txt", "r") as input_file:
        input_text = input_file.read().strip()

    # Translate the input text
    body = [{'text': input_text}]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    # Extract and write translated text to file
    translated_texts = []
    for translation in response:
        translated_texts.append(translation['translations'][0]['text'])

    with open(file_path +"summary_ja.txt", "w") as output_file:
        for text in translated_texts:
            output_file.write(text + "\n")  # Add newline for each translation
    return translated_texts

if __name__ == '__main__':
    trans()
    print("Translation done!")