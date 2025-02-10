from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader

loader = TextLoader("data/faqs.txt")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings, persist_directory="chroma_db")
vectorstore.persist()

print("Knowledge base indexed and saved to 'chroma_db'.")