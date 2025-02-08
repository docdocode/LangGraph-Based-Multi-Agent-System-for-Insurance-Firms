# Insurance Multi-Agent System

This application is a **multi-agent system** designed to handle various types of insurance-related queries using **LangGraph**, an extension of **LangChain**. The system dynamically routes user queries to appropriate agents based on their context, ensuring accurate and relevant responses. It leverages **Retrieval-Augmented Generation (RAG)** for customer support and **DuckDuckGo** for external information retrieval.

---

## Repository Structure

```plaintext
LangGraph-Based-Multi-Agent-System-for-Insurance-Firms/
├── agents/
│   ├── claim_processor.py
│   ├── customer_support.py
│   ├── policy_advisor.py
│   └── tool_agent.py
├── workflows/
│   ├── insurance_workflow.py
│   └── utils.py
├── data/
│   ├── faqs.txt
│   ├── policies.csv
│   └── index_knowledge_base.py
├── images/
│   └── workflow_diagram.png
├── .env
├── .gitignore
├── README.md
├── app.py
├── main.py
├── requirements.txt
└── index_knowledge_base.py
```
---

## Tools, Libraries, and Frameworks Used

### Core Frameworks
- **LangGraph**: Manages the graph-based workflow and state transitions.
- **LangChain**: Provides foundational tools like LLMs, prompts, and tools.

### Language Models
- **OpenAI**: Used for classification, claim processing, policy recommendations, and generating responses.
- **ChatOpenAI**: Invokes OpenAI models like `gpt-3.5-turbo` or `gpt-4`.

### Knowledge Base and Embeddings
- **Chroma**: Vector database for storing embeddings of the knowledge base.
- **OpenAIEmbeddings**: Generates embeddings for the knowledge base.
- **RetrievalQA**: Retrieves relevant information from the knowledge base.

### Web Search
- **duckduckgo-search**: Performs web searches using DuckDuckGo.

### Utilities
- **dotenv**: Loads environment variables from `.env`.
- **requests**: Makes HTTP requests for web searches.
- **tiktoken**: Tokenizer for OpenAI models.

## Workflow Overview

The workflow consists of the following steps:

1. **User Input**: The user provides a query.
2. **Query Classification**: The query is classified into one of four categories:
   - `claim_processing`
   - `policy_recommendation`
   - `customer_support`
   - `tool_task`
3. **Agent Routing**: Based on the classification, the query is routed to the appropriate agent.
4. **Agent Processing**: The selected agent processes the query using its specific logic.
5. **Final Response**: The result from the agent is returned to the user.

---

## Detailed Workflow

### Step 1: User Input
- **Input**: A natural language query from the user.
- **Example Queries**:
  - "My car was damaged in an accident."
  - "I need a policy recommendation for a young driver."
  - "How do I cancel my policy?"
  - "What are the minimum car insurance requirements in Texas?"

### Step 2: Query Classification
- **Node**: `classify_query`
- **Tools/Libraries**:
  - **LangChain**: Used for prompt engineering and LLM interaction.
  - **ChatPromptTemplate**: Formats the classification prompt.
  - **ChatOpenAI**: Invokes the OpenAI model for classification.
- **Logic**:
  The query is passed to an LLM, which classifies it into one of the predefined categories:
  - `claim_processing`: For claims-related queries.
  - `policy_recommendation`: For policy advice.
  - `customer_support`: For FAQs and general support.
  - `tool_task`: For queries requiring external information.
- **Example Prompt**:
  ```plaintext
  Classify the following query into one of these categories:
  claim_processing: Queries related to processing insurance claims (e.g., accidents, incidents).
  policy_recommendation: Queries asking for advice or recommendations on insurance policies.
  customer_support: Queries seeking help or clarification about policies or services.
  tool_task: Queries involving searching for external information or performing a web search (e.g., "find", "search", "latest regulations").
  Query: {query}
  ```
- **Output**: A category label (`claim_processing`, `policy_recommendation`, etc.) that determines the next node.

### Step 3: Agent Routing
- **Graph Structure**: The system uses **LangGraph** to define a directed graph where nodes represent tasks or agents, and edges represent transitions between them.
- **Tools/Libraries**:
  - **LangGraph**: Manages the graph structure and state transitions.
  - **StateGraph**: Defines the graph and adds nodes/edges.
  - **add_conditional_edges**: Specifies conditional transitions based on the classification.
- **Routing Logic**:
  The `route_based_on_category` function determines the next node based on the classification:
  ```python
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
          return END
  ```

### Step 4: Agent Processing
Based on the classification, the query is routed to the appropriate agent:

#### Agent 1: ClaimProcessingAgent
- **Triggered By**: Queries classified as `claim_processing`.
- **Tools/Libraries**:
  - **LangChain**: Used for prompt engineering and LLM interaction.
  - **ChatPromptTemplate**: Formats the prompt for claim processing.
  - **ChatOpenAI**: Invokes the OpenAI model to generate a response.
- **Logic**:
  Processes claims based on incident details.
- **Example Query**: "My car was damaged in an accident."
- **Example Prompt**:
  ```plaintext
  You are an insurance claim processor. Given the policy ID and incident details, determine the validity of the claim and suggest next steps.
  Policy ID: POL12345
  Incident Details: Car accident on highway
  ```
- **Output**: A response about claim validity or next steps.

#### Agent 2: PolicyAdvisorAgent
- **Triggered By**: Queries classified as `policy_recommendation`.
- **Tools/Libraries**:
  - **LangChain**: Used for prompt engineering and LLM interaction.
  - **ChatPromptTemplate**: Formats the prompt for policy recommendations.
  - **ChatOpenAI**: Invokes the OpenAI model to generate a response.
- **Logic**:
  Recommends policies based on customer profiles.
- **Example Query**: "I need a policy recommendation for a young driver."
- **Example Prompt**:
  ```plaintext
  You are a policy advisor. Based on the customer profile, recommend the best insurance policy.
  Customer Profile: Young driver with a clean record
  ```
- **Output**: A recommended policy.

#### Agent 3: CustomerSupportAgent
- **Triggered By**: Queries classified as `customer_support`.
- **Tools/Libraries**:
  - **LangChain**: Used for RAG pipeline and LLM interaction.
  - **Chroma**: Vector database for storing embeddings of the knowledge base.
  - **OpenAIEmbeddings**: Generates embeddings for the knowledge base.
  - **RetrievalQA**: Retrieves relevant information from the knowledge base.
  - **ChatPromptTemplate**: Formats the prompt for generating responses.
  - **ChatOpenAI**: Invokes the OpenAI model to generate a response.
- **Logic**:
  Uses RAG to retrieve relevant information from the knowledge base (`faqs.txt`) and generates a response. If no relevant information is found, it suggests contacting customer support.
- **Example Query**: "How do I cancel my policy?"
- **Example Knowledge Base Entry**:
  ```plaintext
  Q: How do I cancel my policy?
  A: To cancel your policy, contact our customer support team via phone or email.
  ```
- **Output**: An answer from the knowledge base or a fallback message.

#### Agent 4: ToolAgent
- **Triggered By**: Queries classified as `tool_task`.
- **Tools/Libraries**:
  - **LangChain**: Used for tool integration and LLM interaction.
  - **duckduckgo-search**: Performs web searches using DuckDuckGo.
  - **BaseTool**: Defines custom tools for agents.
  - **initialize_agent**: Initializes the agent with tools.
  - **AgentType.OPENAI_FUNCTIONS**: Specifies the agent type.
- **Logic**:
  Performs a web search using DuckDuckGo to fetch external information.
- **Example Query**: "What are the minimum car insurance requirements in Texas?"
- **Output**: Search results from DuckDuckGo.

### Step 5: Final Response
- **Output**: The result from the appropriate agent is returned to the user as the final response.
- **Example Output**:
  ```plaintext
  Using OpenAI Model: gpt-3.5-turbo
  Starting Insurance Multi-Agent System...
  Please describe your query or issue:
  > What are the minimum car insurance requirements in Texas?
  Classified Query Category: tool_task
  Calling Agent: ToolAgent (Web Search)
  It is using web search using DuckDuckGo...
  Workflow Completed. Result: {
      "query": "What are the minimum car insurance requirements in Texas?",
      "results": [
          {"title": "Texas Car Insurance Requirements - DMV", "href": "https://www.dmv.org/..."},
          {"title": "Minimum Car Insurance Coverage in Texas - Nolo", "href": "https://www.nolo.com/..."},
      ]
  }
  ```

---

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/docdocode/LangGraph-Based-Multi-Agent-System-for-Insurance