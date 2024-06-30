from config import IS_LOCAL
import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

deployment_name = st.secrets["DEPLOYMENT_NAME_4o"] if not IS_LOCAL else os.getenv('DEPLOYMENT_NAME_4o')

# Configure Azure OpenAI
llm_chat = AzureOpenAI(
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"] if not IS_LOCAL else os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_key=st.secrets["AZURE_OPENAI_KEY"] if not IS_LOCAL else os.getenv('AZURE_OPENAI_KEY'),
    api_version=st.secrets["API_VERSION"] if not IS_LOCAL else os.getenv('API_VERSION'),
)

def regenerate_lines(lines, lyrics):
    
    print("Lyrics: '" + str(lyrics) + "'")
    
    messages = [
        {
            "role": "system",
            "content": "You are an expert in rewriting lines of a song. You receive complete lyrics from a song and lines that need to be rewritten. You need to rewrite the lines in a creative and engaging way, while maintaining the overall theme and style of the song. You will return only the lines that you have rewritten. You must avoid writing anything else."
        },
        {
            "role": "system",
            "content": "<LYRICS>" + str(lyrics) + "</LYRICS>"
        },
        {
            "role": "user",
            "content": "<LINES>" + "\n".join(lines) + "</LINES>"
        }
    ]

    response = llm_chat.chat.completions.create(messages=messages, model=deployment_name, temperature=0.8)
    
    text = response.choices[0].message.content
    
    print("Risposta LLM: '" + text + "' per set di frasi: '" + str(lines) + "'")
    
    return text.split("\n")