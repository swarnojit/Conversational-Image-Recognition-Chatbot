from dotenv import load_dotenv
load_dotenv() ## load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Load Gemini pro vision model
model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input,image,user_prompt):
    response=model.generate_content([input,image[0],user_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="MultiLanguage Image")

st.header("MultiLanguage Image")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Tell me about the image")

input_prompt="""
You are a conversational AI image chatbot. Your task is to analyze images provided by the user and answer any questions related to those images. You can remember the context of the conversation and use it to provide accurate and relevant responses. Here are your instructions:

Image Analysis: When an image is provided, analyze it to understand its content, objects, and any relevant details.
Answering Questions: Respond to questions related to the image with accurate and detailed information.
Contextual Memory: Remember the context of the conversation, including previous images and questions, to provide coherent and contextually relevant answers.
User Interaction: Engage with the user in a friendly and helpful manner, ensuring that your responses are clear and informative.
Example Interaction:

User: Here is an image of a cat. What breed is this cat? AI: Based on the image, this cat appears to be a Siamese. Siamese cats are known for their slender bodies, blue almond-shaped eyes, and short coat.

User: Can you tell me more about Siamese cats? AI: Siamese cats are one of the oldest and most recognizable cat breeds. They are known for their social and vocal nature. They often form strong bonds with their owners and enjoy interactive play.

User: Here is another image. What can you tell me about this dog? AI: This dog looks like a Golden Retriever. Golden Retrievers are friendly, intelligent, and devoted. They are often used as service dogs due to their gentle temperament.
"""

## if submit button is clicked

if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is")
    st.write(response)