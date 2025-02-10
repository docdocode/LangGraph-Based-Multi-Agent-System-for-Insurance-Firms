from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate

class CustomerSupportAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        
        #Loading the Chroma vector store
        self.vectorstore = Chroma(persist_directory="chroma_db", embedding_function=OpenAIEmbeddings())
        
        self.prompt_template = ChatPromptTemplate.from_template(
            """
            You are a customer support assistant. Use the following context to answer the user's question:
            Context: {context}
            Question: {question}
            Answer:
            """
        )
    
    def handle_query(self, query):
        print("\033[1m\033[93mCalling Agent: CustomerSupportAgent (with RAG)\033[0m")  
        docs = self.vectorstore.similarity_search(query, k=3)  
        context = "\n".join([doc.page_content for doc in docs])
        
        if not context.strip():
            return "I'm sorry, I couldn't find the information you're looking for. Please contact customer support for further assistance."
        
        prompt = self.prompt_template.format(context=context, question=query)
        
        response = self.llm.invoke(prompt)
        return response.content