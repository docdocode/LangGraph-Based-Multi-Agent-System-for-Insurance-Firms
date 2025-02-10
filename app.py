import streamlit as st
from workflows.insurance_workflow import execute_workflow
from dotenv import load_dotenv
import os

load_dotenv()

# Streamlit App Title and Description
st.set_page_config(page_title="Insurance Multi-Agent System", layout="wide")
st.title("🚀 Insurance Multi-Agent System 🚀")
st.markdown("""
Welcome to the **Insurance Multi-Agent System**, powered by LangGraph and OpenAI!  
This application leverages multiple AI agents to assist you with:
- **Claim Processing**: Handle insurance claims efficiently.
- **Policy Recommendations**: Get personalized policy suggestions.
- **Customer Support**: Answer your queries using a knowledge base (RAG).
- **Tool Agent**: Perform web searches for external information.
""")

st.sidebar.header("About the Agents")
st.sidebar.markdown("""
- **ClaimProcessorAgent**: Processes insurance claims based on incident details.
- **PolicyAdvisorAgent**: Recommends policies tailored to customer profiles.
- **CustomerSupportAgent**: Uses RAG to fetch answers from a knowledge base.
- **ToolAgent**: Performs web searches using DuckDuckGo for real-time information.
""")

st.subheader("Ask Your Question")
user_input = st.text_input("Enter your query here:", placeholder="e.g., What does my policy cover?")

if user_input.strip():  # Check if the input is not empty
    if user_input.lower() in ["quit", "exit"]:
        st.warning("Exiting the chat. Goodbye!")
    else:
        # Display the model being used
        model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
        st.info(f"Using OpenAI Model: **{model_name}**")

        # Execute the workflow and capture the response
        with st.spinner("Processing your query..."):
            result, logs = execute_workflow(user_input)

        # Display the workflow logs (only the called agent)
        st.subheader("Workflow Logs")
        st.code(logs, language="plaintext")

        # Stream the LLM output in markdown format
        st.subheader("Response")
        st.markdown(result, unsafe_allow_html=True)