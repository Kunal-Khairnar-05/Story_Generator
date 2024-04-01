import streamlit as st
import requests
from PIL import Image
import io

API_URL_NEO = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
API_URL_STABILITY = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": "Bearer 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"}  # Replace with your API key

def query(API_URL, payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def query_image(API_URL, payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

st.title('Story and Image Generator')

user_input = st.text_area('Enter the starting of the story:')

if st.button('Generate'):
    if user_input:
        # For story generation
        output = query(
            API_URL_NEO,
            {
                "inputs": user_input,
                "parameters": {
                    "min_length": 1000,
                    "do_sample": False
                }
            })[0]["generated_text"]

        # For image generation
        output1 = query_image(
            API_URL_STABILITY,
            {
                "inputs": user_input,
            }
        )

        im = Image.open(io.BytesIO(output1))
        im.save("image.jpg")

        st.subheader('Generated Story:')
        st.write(output)

        st.subheader('Generated Image:')
        st.image("image.jpg")
    else:
        st.warning('Please enter the starting of the story.')
