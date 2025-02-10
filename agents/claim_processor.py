from utils.config import get_llm
from utils.prompts import CLAIM_PROCESSING_PROMPT

class ClaimProcessorAgent:
    def __init__(self):
        self.llm = get_llm()  
    def process_claim(self, policy_id, incident_details):
        prompt = CLAIM_PROCESSING_PROMPT.format(policy_id=policy_id, incident_details=incident_details)
        print("\033[1m\033[93mCalling Agent: ClaimProcessorAgent\033[0m")
        response = self.llm.invoke(prompt) 
        
        llm_response_content = response.content if hasattr(response, "content") else str(response)
        return llm_response_content