from ollama import Client
from retrieve_context import retrieveVectorStore
from dotenv import load_dotenv

load_dotenv()


ollama_llm = Client(host='http://localhost:11434')
gemma_llm = 'gemma2:2btest'
llama_llm = 'llama3.2test'

query = 'Wie erstelle ich ein Datenobjekt?'
context = retrieveVectorStore(query, False, 4)
localllm_prompt_template = """
Beantworte mir auf folgenden Kontext die Frage: {query}

Kontext: {context}
"""
llm_query = localllm_prompt_template.format(query=query, context=context)