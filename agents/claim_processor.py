from utils.config import get_llm
from utils.prompts import CLAIM_PROCESSING_PROMPT

class ClaimProcessorAgent:
    def __init__(self):
        self.llm = get_llm()  # Use the centralized model
    
    def process_claim(self, policy_id, incident_details):
        prompt = CLAIM_PROCESSING_PROMPT.format(policy_id=policy_id, incident_details=incident_details)
        response = self.llm.invoke(prompt)
        return response