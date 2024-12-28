from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
import os
from dotenv import load_dotenv

# Retrieve relevant information from Vector Search as a single str

def mongoDB_as_retriever(k: int):
    load_dotenv()
    # Load the embedding model
    embed_model = GoogleGenerativeAIEmbeddings(google_api_key=os.getenv('GOOGLE_API_KEYy'), model="models/text-embedding-004")

    # Connect to MongoDB Atlas Vector Search
    uri = os.getenv('MONGO_DB_URI')
    namespace = os.getenv('MONGO_DB')
    vector_store = MongoDBAtlasVectorSearch.from_connection_string(
        connection_string = uri,
        namespace = namespace,
        embedding = embed_model
    )

    return vector_store.as_retriever(
        search_type = 'similarity',
        search_kwargs={'k': k},
        score_threshhold = .95
    )

def retrieveVectorStore(search_query: str, as_list: bool, k: int):
    retriever = mongoDB_as_retriever(k)
    relDocs = retriever.invoke(search_query)
    if as_list:
        return relDocs
    
    docs_str = ''
    for doc in relDocs:
        docs_str += doc.page_content + '\n'
    return docs_str