import argparse
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama



from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from get_embeddings_function import get_embeddings


CHROMA_PATH = "chroma"


PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""




def main():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('query_text', type= str, help = 'The query text.')
    args = parser.parse_args()
    query_text = args.query_text
    
    
    query_rag(query_text)
    
def query_rag(query_text:str):
    
    embedding_function = get_embeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_score(query_text, k=3)

   # print(results)
    # if len(results) == 0 or results[0][1] < 0.7:
    #     print(f"Unable to find matching results")
    #     return
    # print(results[0])
    

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question = query_text)
    
    print(prompt)
    
    print('\n\n\n\n')

    
    model = Ollama(model='mistral')
    response_text = model.invoke(prompt)
    
    sources = [doc.metadata.get('id', None) for doc, _score in results]
    
    formatted_response = f"Response: {response_text}\n\n----\n\nSources: {sources}"
    print(formatted_response)

    return response_text


if __name__ == "__main__":
    main()