from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from get_embeddings_function import get_embeddings
from langchain_community.vectorstores import Chroma
import os
import shutil
import argparse


DATA_PATH = 'data/books'
CHROMA_PATH = 'chroma'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true', help='Reset the database')
    args = parser.parse_args()
    if args.reset:
        print("......Database is deleted......")
        clear_database()
        
    documents = load_documents()
    chunks = split_documents(documents)
    print(len(documents))
    save_to_chroma(chunks)  
    
def load_documents():
    
    text_loader_kwargs={'autodetect_encoding': True}
    
    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    return documents



def save_to_chroma(chunks: list[Document]): # type: ignore
 
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embeddings()
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    
    
    chunks_with_ids = calculate_chunk_ids(chunks)
    
      
    # Add or Update the documents.
    existing_items = db.get(include=[])
    existing_ids = set(existing_items['ids'])
    
    print(f"Number of existing documents in DB: {len(existing_ids)}")
    
    
    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("✅ No new documents to add")


    

    
def calculate_chunk_ids(chunks):
    last_page_id =None
    current_chunk_index = 0
    for chunk in chunks:
        source = chunk.metadata.get('source')
        page = chunk.metadata.get('page')
        current_page_id = f'{source}:{page}'
        
        if current_page_id == last_page_id:
            current_chunk_index+=1
        else:
            current_chunk_index = 0
            
        chunk_id = f'{current_page_id}:{current_chunk_index}'
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id
        
    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 200,
        length_function = len,
        add_start_index= True,
        )

    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks")
    
    return chunks

def split_documents(documents:list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 200,
        length_function = len,
        is_separator_regex=False,
    )
    
    return text_splitter.split_documents(documents)



if __name__ == "__main__":
    main()