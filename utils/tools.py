from langchain.tools import BaseTool
from duckduckgo_search import DDGS

class WebSearchTool(BaseTool):
    name: str = "web_search_tool"  
    description: str = "A tool for performing web searches"

    def _run(self, query: str):
        """
        Perform a DuckDuckGo search and return the summary of the top results. And add all the reference link at the end of the summary.
        :param query: The search query.
        :return: The summary, and the reference links.
        """
        try:
            with DDGS() as ddgs:
                results = [result for result in ddgs.text(query, max_results=5)] 
                if results:
                    return {
                        "query": query,
                        "results": results
                    }
                else:
                    return f"No results found for query: {query}"
        except Exception as e:
            return f"An error occurred during the search: {str(e)}"

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported")