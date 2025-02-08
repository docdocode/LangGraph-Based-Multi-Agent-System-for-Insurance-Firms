from agents.claim_processor import ClaimProcessorAgent
from agents.policy_advisor import PolicyAdvisorAgent
from agents.customer_support import CustomerSupportAgent
from agents.tool_agent import ToolAgent
from agents.supervisor_agent import SupervisorAgent

class InsuranceWorkflow:
    def __init__(self):
        # Initialize agents
        self.claim_processor = ClaimProcessorAgent()
        self.policy_advisor = PolicyAdvisorAgent()
        self.customer_support = CustomerSupportAgent()
        self.tool_agent = ToolAgent()
        
        # Supervisor agent to orchestrate tasks
        self.supervisor = SupervisorAgent({
            "claim_processor": self.claim_processor,
            "policy_advisor": self.policy_advisor,
            "customer_support": self.customer_support,
            "tool_agent": self.tool_agent
        })
    
    def execute(self, task):
        return self.supervisor.assign_task(task)