from workflows.insurance_workflow import execute_workflow
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")  # Default to gpt-3.5-turbo
    print(f"\033[1m\033[94mUsing OpenAI Model: {model_name}\033[0m")  
    
    print("Starting Insurance Multi-Agent System...")
    print("\033[1m\033[93mType 'quit' or 'exit' to end the conversation.\033[0m")  
    
    while True:
        print("\n\033[1;34mPlease describe your query or issue:\033[0m")
        user_input = input("\033[1;33m> \033[0m").strip()
        
        if user_input.lower() in ["quit", "exit", "clear", "done", "bye"]:
            print("\033[1m\033[91mExiting the chat. Goodbye!\033[0m")
            break
        
        result, logs = execute_workflow(user_input)
        
        # Print the response, calling agent, and category separately
        print("\033[1m\033[92mResponse:\033[0m", result) 

if __name__ == "__main__":
    main()