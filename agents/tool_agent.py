from langchain.agents import initialize_agent, AgentType
from utils.config import get_llm
from utils.tools import WebSearchTool

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
        return self.agent.run(task_description)