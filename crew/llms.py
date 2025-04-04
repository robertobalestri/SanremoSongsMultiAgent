from config import IS_LOCAL

if not IS_LOCAL:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import streamlit as st
from langchain_openai import AzureChatOpenAI


from dotenv import load_dotenv

if IS_LOCAL:
    load_dotenv()
    azure_llm_4_turbo = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("API_VERSION"),
        deployment_name=os.getenv("DEPLOYMENT_NAME_4_TURBO"),
        temperature=1
    )

    azure_llm_4_turbo_low_temperature = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("API_VERSION"),
        deployment_name=os.getenv("DEPLOYMENT_NAME_4_TURBO"),
        temperature=0.2
    )

    azure_llm_4o = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("API_VERSION"),
        deployment_name=os.getenv("DEPLOYMENT_NAME_4o"),
        temperature=1
    )
else:
    azure_llm_4_turbo = AzureChatOpenAI(
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
        api_key=st.secrets["AZURE_OPENAI_KEY"],
        api_version=st.secrets["API_VERSION"],
        deployment_name=st.secrets["DEPLOYMENT_NAME_4_TURBO"],
        temperature=1
    )

    azure_llm_4_turbo_low_temperature = AzureChatOpenAI(
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
        api_key=st.secrets["AZURE_OPENAI_KEY"],
        api_version=st.secrets["API_VERSION"],
        deployment_name=st.secrets["DEPLOYMENT_NAME_4_TURBO"],
        temperature=0.2
    )

    azure_llm_4o = AzureChatOpenAI(
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
        api_key=st.secrets["AZURE_OPENAI_KEY"],
        api_version=st.secrets["API_VERSION"],
        deployment_name=st.secrets["DEPLOYMENT_NAME_4o"],
        temperature=1
    )
