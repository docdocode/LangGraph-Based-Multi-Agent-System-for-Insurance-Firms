from utils.config import get_llm
from utils.prompts import CUSTOMER_SUPPORT_PROMPT

class CustomerSupportAgent:
    def __init__(self):
        self.llm = get_llm()  # Use the centralized model
    
    def handle_query(self, query):
        prompt = CUSTOMER_SUPPORT_PROMPT.format(query=query)
        response = self.llm.invoke(prompt)
        return response