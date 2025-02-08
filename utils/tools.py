import requests
from langchain.tools import BaseTool
import os

class WebSearchTool(BaseTool):
    name: str = "web_search_tool"
    description: str = "A tool for performing web searches"

    def _run(self, query: str):
        # Use SerpAPI for web search
        api_key = os.getenv("SERPAPI_API_KEY")
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}"

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported")