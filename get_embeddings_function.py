from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings


def get_embeddings():

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    return embeddings