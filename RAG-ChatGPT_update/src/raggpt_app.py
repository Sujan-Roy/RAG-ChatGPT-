"""
    This module uses Gradio to create an interactive web app for a chatbot with various features.

    The app's interface is split into three sections:
    1. The first section contains a Chatbot component that simulates a conversation with a language model, and a hidden
    reference bar that can be shown using a button. The chatbot supports feedback through like and dislike icons.

    2. The second section includes a Textbox for user input. Users can either type text or upload PDF/doc files.

    3. The third section has buttons for submitting text, toggling the reference bar's visibility, uploading PDF/doc files,
    adjusting the GPT responses' temperature, selecting the document type, and clearing the input.

    The app manages user interactions as follows:
    - Uploading files triggers the processing of the files, updating the input and chatbot components.
    - Submitting text causes the chatbot to respond, considering the selected document type and temperature settings.
    The response is displayed in the Textbox and Chatbot components, and the reference bar may be updated.

    The app can be run as a standalone script, launching the Gradio interface for users to interact with the chatbot.

    Note: The docstring provides an overview of the module's purpose and functionality, while detailed comments within the code
    explain specific components, interactions, and logic throughout the implementation.
"""
"""
If You have any questions or need help, please contact me at https://www.linkedin.com/in/dr-sujan-chandra-roy-ph-d-381131109/.
"""

import gradio as gr
from chatbot import ChatBot
from ui_settings import UISettings
from upload_file import UploadFile
from translation import Translator
import os
# Call the Translator class to translate the text
translator = Translator()
file_path = "results/"
        # store the summary in a file in the current directory

if os.path.exists(file_path + "summary_ja.txt"):
    os.remove(file_path + "summary_ja.txt")


with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("RAG-ChatGPT"):
            ##############
            # First ROW:
            ##############
            with gr.Row() as row_one:
                with gr.Column(visible=False) as reference_bar:
                    ref_output = gr.Textbox(
                        lines=22,
                        max_lines=22,
                        interactive=False,
                        type="text",
                        label="References",
                        show_copy_button=True
                    )

                with gr.Column() as chatbot_output:
                    chatbot = gr.Chatbot(
                        [],
                        elem_id="chatbot",
                        bubble_full_width=False,
                        height=500,
                        avatar_images=(
                            ("images/AI_RT.png"), "images/openai_.png"),
                        # render=False
                    )
                    # **Adding like/dislike icons
                    chatbot.like(UISettings.feedback, None, None)
            ##############
            # SECOND ROW:
            ##############
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=4,
                    scale=8,
                    placeholder="Enter your query about the uploaded document and press enter",
                    container=False,
                )

            ##############
            # Third ROW:
            ##############
            with gr.Row() as row_two:
                text_submit_btn = gr.Button(value="Submit text")
                sidebar_state = gr.State(False)
                btn_toggle_sidebar = gr.Button(
                    value="References")
                btn_toggle_sidebar.click(UISettings.toggle_sidebar, [sidebar_state], [
                    reference_bar, sidebar_state])
                upload_btn = gr.UploadButton(
                    "📁 Upload PDF or doc files from user location ", file_types=[
                        '.pdf',
                        '.doc'
                    ],
                    file_count="multiple")
                #translation_btn = gr.Button()
                rag_with_dropdown = gr.Dropdown(
                    label="RAG with", choices=["Preprocessed doc", "Upload doc: Process for RAG", "Upload doc: Give Full summary"], value="Preprocessed doc")
                clear_button = gr.ClearButton([input_txt, chatbot])
            ##############
            # Process:
            ##############
            file_msg = upload_btn.upload(fn=UploadFile.process_uploaded_files, inputs=[
                upload_btn, chatbot, rag_with_dropdown], outputs=[input_txt, chatbot], queue=False)

            txt_msg = input_txt.submit(fn=ChatBot.respond,
                                       inputs=[chatbot, input_txt,
                                               rag_with_dropdown],
                                       outputs=[input_txt,
                                                chatbot, ref_output],
                                       queue=False).then(lambda: gr.Textbox(interactive=True),
                                                         None, [input_txt], queue=False)

            txt_msg = text_submit_btn.click(fn=ChatBot.respond,
                                            inputs=[chatbot, input_txt,
                                                    rag_with_dropdown],
                                            outputs=[input_txt,
                                                     chatbot, ref_output],
                                            queue=False).then(lambda: gr.Textbox(interactive=True),
                                                              None, [input_txt], queue=False)
          

    # # Read a file from the user's location and process it
    # # Read input text from a file
    #         file_path = "results/"
    #         with open(file_path +"summary_ja.txt", "r") as input_file:
    #             trans_text = input_file.read().strip()  
        
    #         # show the trans_text by clicking the translation button
            # Show the translated text by clicking the translation button
           # translation_btn.click(fn=lambda: display_translated_text(), outputs=[])


    def display_translated_text():
        """Reads the translated text from the file """
        file_path = "results/"
        # Delete the file if it exists
        try:
            with open(file_path + "summary_ja.txt", "r") as input_file:
                trans_text = input_file.read().strip()
                # Update the reference bar with the translated text
                #ref_output.value = trans_text 
                return trans_text
        except FileNotFoundError:
            print("Translated text file not found.")

   # Show the translated text by clicking the translation button
    translation_btn = gr.Interface(fn=display_translated_text, inputs=[], outputs="text",flagging_options=None)
    # translation_btn = gr.Button(value="Translate")  # Using gr.Button for a button style
    # translation_btn.click(fn=display_translated_text, outputs=["text"])  # Link click to function
    #btn= gr.Button(value="Show translation")
    # btn = gr.inputs.Button(label="Translate")
    # translation = btn(fn=display_translated_text, inputs=[], outputs="text")
    

if __name__ == "__main__":
    demo.launch()
   
