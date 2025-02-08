from utils.config import get_llm
from utils.prompts import POLICY_ADVISOR_PROMPT

class PolicyAdvisorAgent:
    def __init__(self):
        self.llm = get_llm()  # Use the centralized model
    
    def recommend_policy(self, customer_profile):
        prompt = POLICY_ADVISOR_PROMPT.format(customer_profile=customer_profile)
        response = self.llm.invoke(prompt)
        return response