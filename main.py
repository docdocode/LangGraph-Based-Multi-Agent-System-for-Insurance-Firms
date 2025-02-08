from workflows.insurance_workflow import InsuranceWorkflow
from dotenv import load_dotenv
import os

# Explicitly specify the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
print(f"Loading .env file from: {dotenv_path}")
load_dotenv(dotenv_path)

# Debug: Print the API key to verify it's loaded
# print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

def main():
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")  # Default to gpt-3.5-turbo
    print(f"\033[1m\033[94mUsing OpenAI Model: {model_name}\033[0m")  # Bold and blue text
    
    print("Starting Insurance Multi-Agent System...")
    
    # Initialize the workflow
    workflow = InsuranceWorkflow()
    
    # Example task: Process a claim
    task = {
        "type": "claim_processing",
        "data": {
            "policy_id": "POL12345",
            "incident_details": "Car accident on highway"
        }
    }
    
    # Execute the workflow
    result = workflow.execute(task)
    print("\033[1m\033[92mWorkflow Completed. Result:\033[0m", result)  # Bold and green text

if __name__ == "__main__":
    main()