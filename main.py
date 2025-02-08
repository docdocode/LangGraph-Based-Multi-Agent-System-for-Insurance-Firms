from workflows.insurance_workflow import execute_workflow
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def main():
    # Print the model being used
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")  # Default to gpt-3.5-turbo
    print(f"\033[1m\033[94mUsing OpenAI Model: {model_name}\033[0m")  # Bold and blue text
    
    print("Starting Insurance Multi-Agent System...")
    print("\033[1m\033[93mType 'quit' or 'exit' to end the conversation.\033[0m")  # Instructions for quitting
    
    while True:
        # Take input from the user
        print("\nPlease describe your query or issue:")
        user_input = input("> ").strip()
        
        # Check if the user wants to quit
        if user_input.lower() in ["quit", "exit", "clear", "done", "bye"]:
            print("\033[1m\033[91mExiting the chat. Goodbye!\033[0m")
            break
        
        # Execute the workflow
        result, logs = execute_workflow(user_input)
        
        # Print the response, calling agent, and category separately
        print("\033[1m\033[92mWorkflow Completed. Response:\033[0m", result)  # Bold and green text
        # print("\033[1m\033[94mWorkflow Logs:\033[0m", logs)  # Bold and blue text

if __name__ == "__main__":
    main()