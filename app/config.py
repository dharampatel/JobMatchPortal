import os
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=os.getenv('GOOGLE_API_KEY'))