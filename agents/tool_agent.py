from langchain.agents import initialize_agent, AgentType
from utils.config import get_llm
from utils.tools import WebSearchTool
import os

class ToolAgent:
    def __init__(self):
        self.llm = get_llm()  # Use the centralized model
        # Define the web search tool
        self.web_search_tool = WebSearchTool()
        # Initialize the agent with the web search tool
        self.agent = initialize_agent(
            tools=[self.web_search_tool],
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )

    def execute_task(self, task_description):
        """
        Executes a task using OpenAI's function calling and the web search tool.
        :param task_description: A natural language description of the task.
        :return: The result of the task execution.
        """
        # Check if the query is related to insurance
        if not self.is_insurance_related(task_description):
            return "I'm sorry, but this query is outside my expertise. I can only assist with questions related to insurance and insurance policies."

        print("\033[1m\033[96mIt is using web search using DuckDuckGo...\033[0m")  # Bold and cyan text
        return self.agent.run(task_description)

    def is_insurance_related(self, query):
        """
        Determines if the query is related to insurance or insurance policies.
        :param query: The user's query.
        :return: True if the query is insurance-related, False otherwise.
        """
        # List of keywords related to insurance
        insurance_keywords = [
            "insurance", "policy", "coverage", "claim", "premium", "deductible",
            "liability", "car insurance", "health insurance", "home insurance",
            "life insurance", "regulations", "requirements"
        ]
        # Check if any keyword is present in the query
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in insurance_keywords)