from utils.config import get_llm
from utils.prompts import POLICY_ADVISOR_PROMPT

class PolicyAdvisorAgent:
    def __init__(self):
        self.llm = get_llm() 
    
    def recommend_policy(self, customer_profile):
        prompt = POLICY_ADVISOR_PROMPT.format(customer_profile=customer_profile)
        print("\033[1m\033[93mCalling Agent: PolicyAdvisorAgent\033[0m")
        response = self.llm.invoke(prompt)
        llm_response_content = response.content if hasattr(response, "content") else str(response)
        return llm_response_content