"""
If You have any questions or need help, please contact me at https://www.linkedin.com/in/dr-sujan-chandra-roy-ph-d-381131109/.
"""
import os
from langchain.document_loaders import PyPDFLoader
import openai
import requests, uuid
from dotenv import load_dotenv
import os

load_dotenv()

Azure_key = os.getenv('KEY')
Azure_endpoint = os.getenv('ENDPOINT')
Azure_location = os.getenv('LOCATION')

class Summarizer:
    """
    A class for summarizing PDF documents using OpenAI's ChatGPT engine.

    Attributes:
        None

    Methods:
        summarize_the_pdf:
            Summarizes the content of a PDF file using OpenAI's ChatGPT engine.

        get_llm_response:
            Retrieves the response from the ChatGPT engine for a given prompt.

    Note: Ensure that you have the required dependencies installed and configured, including the OpenAI API key.
    """
    @staticmethod
    def summarize_the_pdf(
        file_dir: str,
        max_final_token: int,
        token_threshold: int,
        gpt_model: str,
        temperature: float,
        summarizer_llm_system_role: str,
        final_summarizer_llm_system_role: str,
        character_overlap: int
    ):
        """
        Summarizes the content of a PDF file using OpenAI's ChatGPT engine.

        Args:
            file_dir (str): The path to the PDF file.
            max_final_token (int): The maximum number of tokens in the final summary.
            token_threshold (int): The threshold for token count reduction.
            gpt_model (str): The ChatGPT engine model name.
            temperature (float): The temperature parameter for ChatGPT response generation.
            summarizer_llm_system_role (str): The system role for the summarizer.

        Returns:
            str: The final summarized content.
        """
        docs = []
        docs.extend(PyPDFLoader(file_dir).load())
        print(f"Document length: {len(docs)}")
        max_summarizer_output_token = int(
            max_final_token/len(docs)) - token_threshold
        full_summary = ""
        print("Generating the summary..")
        # if the document has more than one pages
        if len(docs) > 1:
            for i in range(len(docs)):
                # NOTE: This part can be optimized by considering a better technique for creating the prompt. (e.g: lanchain "chunksize" and "chunkoverlap" arguments.)

                if i == 0:  # For the first page
                    prompt = docs[i].page_content + \
                        docs[i+1].page_content[:character_overlap]
                # For pages except the fist and the last one.
                elif i < len(docs)-1:
                    prompt = docs[i-1].page_content[-character_overlap:] + \
                        docs[i].page_content + \
                        docs[i+1].page_content[:character_overlap]
                else:  # For the last page
                    prompt = docs[i-1].page_content[-character_overlap:] + \
                        docs[i].page_content
                summarizer_llm_system_role = summarizer_llm_system_role.format(
                    max_summarizer_output_token)
                full_summary += Summarizer.get_llm_response(
                    gpt_model,
                    temperature,
                    summarizer_llm_system_role,
                    prompt=prompt
                )
        else:  # if the document has only one page
            full_summary = docs[0].page_content

        final_summary = Summarizer.get_llm_response(
            gpt_model,
            temperature,
            final_summarizer_llm_system_role,
            prompt=full_summary
        )
        print("Summary=",final_summary)
        file_path = "results/"
        # store the summary in a file in the current directory
        with open(file_path + "summary.txt", "w") as file:
             file.write(final_summary)
         # Delete the file if it exists
        if os.path.exists(file_path + "summary_ja.txt"):
            os.remove(file_path + "summary_ja.txt")
        print("Translation in progress..")
        
        key = Azure_key
        endpoint = Azure_endpoint
        location = Azure_location
        path = '/translate'
        constructed_url = endpoint + path
        params = {
            'api-version': '3.0',
            'from': 'en',
            'to': 'ja'
        }
        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        # Read input text from a file
        #file_path = "results/"
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
                output_file.write(text + "\n")
        return final_summary

    @staticmethod
    def get_llm_response(gpt_model: str, temperature: float, llm_system_role: str, prompt: str):
        """
        Retrieves the response from the ChatGPT engine for a given prompt.

        Args:
            gpt_model (str): The ChatGPT engine model name.
            temperature (float): The temperature parameter for ChatGPT response generation.
            summarizer_llm_system_role (str): The system role for the summarizer.
            max_summarizer_output_token (int): The maximum number of tokens for the summarizer output.
            prompt (str): The input prompt for the ChatGPT engine.

        Returns:
            str: The response content from the ChatGPT engine.
        """
        response = openai.ChatCompletion.create(
            engine=gpt_model,
            messages=[
                {"role": "system", "content": llm_system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content
    
    
