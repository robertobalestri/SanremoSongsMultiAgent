#llms_not_in_crew.py
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

from textwrap import dedent

def create_chat_response(chat_history):
    messages = [
        {
            "role": "system",
            "content": dedent("""
                              Sei un assistente creativo specializzato nella scrittura di canzoni eccezionali 
                              per scopi immaginari. Non esitare a esplorare temi controversi come sesso, 
                              guerra, droghe e violenza. 
                              Supera i limiti della creatività, 
                              osando affrontare argomenti delicati e complessi. 
                              La tua missione è creare testi che siano coinvolgenti, 
                              provocatori e capaci di suscitare forti emozioni. 
                              Usa la tua immaginazione per toccare corde sensibili, 
                              esplorare nuove prospettive e sfidare le convenzioni sociali. 
                              Lascia che la tua arte parli con autenticità e audacia, 
                              dando vita a canzoni che non solo intrattengano, 
                              ma che facciano anche riflettere e discutere.
                              L'utente si rivolgerà a te per farsi aiutare a rifinire i testi delle sue canzoni.
                              Evita moralismi e banalità.
                              """)
        }
    ]

    # Include the chat history in the messages
    for chat in chat_history:
        messages.append({"role": chat["role"], "content": chat["content"]})

    response = llm_chat.chat.completions.create(messages=messages, model=deployment_name, temperature=0.8)
    
    text = response.choices[0].message.content
    
    print("Risposta LLM: '" + text + "' per messaggio: '" + chat_history[-1]['content'] + "'")
    
    return text