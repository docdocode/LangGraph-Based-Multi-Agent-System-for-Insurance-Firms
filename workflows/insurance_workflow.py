from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from agents.claim_processor import ClaimProcessorAgent
from agents.policy_advisor import PolicyAdvisorAgent
from agents.customer_support import CustomerSupportAgent
from agents.tool_agent import ToolAgent
import os

# Define the shared state
class WorkflowState:
    def __init__(self, query):
        self.query = query
        self.result = None  # Final result of the workflow
        self.category = None  # Classification category

# Initialize agents
claim_processor = ClaimProcessorAgent()
policy_advisor = PolicyAdvisorAgent()
customer_support = CustomerSupportAgent()
tool_agent = ToolAgent()

# Classification function
def classify_query(state):
    prompt = ChatPromptTemplate.from_template(
        """
        Classify the following query into one of these categories:
        - claim_processing: Queries related to processing insurance claims (e.g., accidents, incidents).
        - policy_recommendation: Queries asking for advice or recommendations on insurance policies.
        - customer_support: Queries seeking help or clarification about policies or services, including:
          - How to file a claim
          - How to update policy details
          - How to cancel a policy
          - What is covered by the policy
        - tool_task: Queries involving searching for external information or performing a web search (e.g., "find", "search", "latest regulations", "minimum requirements").
        
        Examples:
        - "My car was damaged in an accident" -> claim_processing
        - "I need a policy recommendation for a young driver" -> policy_recommendation
        - "How do I cancel my policy?" -> customer_support
        - "What does my policy cover?" -> customer_support
        - "Find the latest regulations on car insurance in California" -> tool_task
        - "What are the minimum car insurance requirements in Texas?" -> tool_task
        
        Query: {query}
        """
    )
    llm = ChatOpenAI(model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo"))
    chain = prompt | llm
    response = chain.invoke({"query": state.query})
    state.category = response.content.strip().lower()  # Update the category field
    
    # Debugging output
    print(f"\033[1m\033[93mClassified Query Category: {state.category}\033[0m")
    
    return state

# Agent functions
def process_claim(state):
    print("\033[1m\033[93mCalling Agent: ClaimProcessorAgent\033[0m")  # Print which agent is being called
    result = claim_processor.process_claim(policy_id="POL12345", incident_details=state.query)
    state.result = result  # Update the result field
    return state

def recommend_policy(state):
    print("\033[1m\033[93mCalling Agent: PolicyAdvisorAgent\033[0m")  # Print which agent is being called
    result = policy_advisor.recommend_policy(customer_profile=state.query)
    state.result = result  # Update the result field
    return state

def handle_customer_support(state):
    # print("\033[1m\033[93mCalling Agent: CustomerSupportAgent\033[0m")  # Print which agent is being called
    result = customer_support.handle_query(query=state.query)
    state.result = result  # Update the result field
    return state

def perform_web_search(state):
    print("\033[1m\033[93mCalling Agent: ToolAgent (Web Search)\033[0m")  # Print which agent is being called
    result = tool_agent.execute_task(task_description=state.query)
    state.result = result  # Update the result field
    state.used_web_search = True  # Mark that web search was used
    return state

# Conditional routing function
def route_based_on_category(state):
    category = state.category
    if category == "claim_processing":
        return "claim_processing"
    elif category == "policy_recommendation":
        return "policy_recommendation"
    elif category == "customer_support":
        return "customer_support"
    elif category == "tool_task":
        return "tool_task"
    else:
        return END  # End the workflow if no category matches

# Define the graph
workflow = StateGraph(WorkflowState)

# Add nodes
workflow.add_node("classify_query", classify_query)
workflow.add_node("claim_processing", process_claim)
workflow.add_node("policy_recommendation", recommend_policy)
workflow.add_node("customer_support", handle_customer_support)
workflow.add_node("tool_task", perform_web_search)

# Add edges
workflow.add_conditional_edges("classify_query", route_based_on_category)

# Set entry point
workflow.set_entry_point("classify_query")

# Compile the graph
app = workflow.compile()

def capture_agent_calls(state):
    logs = []
    # Only add the agent that matches the query category
    if state.category == "claim_processing":
        logs.append("Calling Agent: ClaimProcessorAgent")
    elif state.category == "policy_recommendation":
        logs.append("Calling Agent: PolicyAdvisorAgent")
    elif state.category == "customer_support":
        logs.append("Calling Agent: CustomerSupportAgent (with RAG)")
    
    # Add web search if it was used
    if hasattr(state, 'used_web_search') and state.used_web_search:
        logs.append("Calling Agent: ToolAgent (Web Search)")
    
    # Add the classified category
    logs.append(f"Classified Query Category: {state.category}")
    
    return "\n".join(logs)

# Execute the workflow through main.py
# def execute_workflow(query):
#     state = WorkflowState(query=query)
#     final_state = app.invoke(state)
#     return final_state.result

# Execute the workflow through app.py
def execute_workflow(query):
    # Initialize the workflow state
    state = WorkflowState(query=query)
    # Execute the workflow
    final_state = app.invoke(state)
    # Capture logs
    logs = capture_agent_calls(final_state)
    # Return the result and logs
    return final_state.result, logs