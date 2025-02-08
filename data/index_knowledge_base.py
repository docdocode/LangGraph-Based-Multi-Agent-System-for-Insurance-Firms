from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader

# Load the knowledge base
loader = TextLoader("data/faqs.txt")
documents = loader.load()

# Split the text into chunks
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Generate embeddings and store in Chroma
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings, persist_directory="chroma_db")
vectorstore.persist()

print("Knowledge base indexed and saved to 'chroma_db'.")