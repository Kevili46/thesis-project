from langchain_community.document_loaders import TextLoader
from dataset_creator import SRC_FILE
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from custom_splitter import split_by_faq

def upload_doc():

    load_dotenv()
    loader = TextLoader(SRC_FILE)

    data = loader.load()
    docs = split_by_faq(data)

    # Load the embedding model
    embed_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    # Connect to MongoDB Atlas Vector Search
    uri = os.getenv('MONGO_DB_URI')
    client = MongoClient(uri)
    namespace = os.getenv('MONGO_DB')
    vector_store = MongoDBAtlasVectorSearch.from_connection_string(
        connection_string = uri,
        namespace = namespace,
        embedding = embed_model
    )

    # delete all collection entries
    client['LAM-Kevin']['vectorbase'].delete_many({})
    print('cleared')

    # Store the docs as vector embeddings in collection
    vector_store.add_documents(docs)
    print('uploaded')