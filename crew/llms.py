from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import os


load_dotenv()

azure_llm_4_turbo = AzureChatOpenAI(
    azure_endpoint= os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key= os.environ.get("AZURE_OPENAI_KEY"),
    api_version= os.environ.get("API_VERSION"),
    deployment_name = os.environ.get("DEPLOYMENT_NAME_4_TURBO"),
    temperature=1
)

azure_llm_4_turbo_low_temperature = AzureChatOpenAI(
    azure_endpoint= os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key= os.environ.get("AZURE_OPENAI_KEY"),
    api_version= os.environ.get("API_VERSION"),
    deployment_name = os.environ.get("DEPLOYMENT_NAME_4_TURBO"),
    temperature=0.2
)


azure_llm_4o = AzureChatOpenAI(
    azure_endpoint= os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key= os.environ.get("AZURE_OPENAI_KEY"),
    api_version= os.environ.get("API_VERSION"),
    deployment_name = os.environ.get("DEPLOYMENT_NAME_4o"),
    temperature=1
)
