class SupervisorAgent:
    def __init__(self, agents):
        self.agents = agents
    
    def assign_task(self, task):
        # Log which agent is being called
        if task["type"] == "claim_processing":
            print(f"\033[1m\033[93mCalling Agent: ClaimProcessorAgent\033[0m")  # Bold and yellow text
            return self.agents["claim_processor"].process_claim(**task["data"])
        elif task["type"] == "policy_recommendation":
            print(f"\033[1m\033[93mCalling Agent: PolicyAdvisorAgent\033[0m")  # Bold and yellow text
            return self.agents["policy_advisor"].recommend_policy(**task["data"])
        elif task["type"] == "customer_support":
            print(f"\033[1m\033[93mCalling Agent: CustomerSupportAgent\033[0m")  # Bold and yellow text
            return self.agents["customer_support"].handle_query(**task["data"])
        elif task["type"] == "tool_task":
            print(f"\033[1m\033[93mCalling Agent: ToolAgent\033[0m")  # Bold and yellow text
            return self.agents["tool_agent"].execute_task(task["description"])
        else:
            raise ValueError("Unknown task type")