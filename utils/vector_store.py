import os
import shutil
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from utils.config import (
    CHUNK_SIZE, CHUNK_OVERLAP, VECTORSTORE_DIR, 
    EMBEDDING_MODEL, EMBEDDING_BATCH_SIZE
)

def get_embeddings():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    return OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=api_key)

def create_vector_store(documents, repo_id):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)

    embeddings = get_embeddings()

    persist_dir = os.path.join(VECTORSTORE_DIR, repo_id)
    
    if os.path.exists(persist_dir):
        try:
            shutil.rmtree(persist_dir)
            print("Existing vector store removed successfully.")
        except Exception as e:
            print(f"Warning: Could not remove directory: {e}")
    
    total_chunks = len(chunks)

    first_batch = chunks[:EMBEDDING_BATCH_SIZE]
    db = Chroma.from_documents(
        first_batch,
        embeddings,
        persist_directory=persist_dir
    )
    
    for i in range(EMBEDDING_BATCH_SIZE, total_chunks, EMBEDDING_BATCH_SIZE):
        batch = chunks[i : i + EMBEDDING_BATCH_SIZE]
        print(f"Embedding batch {i} to {min(i + EMBEDDING_BATCH_SIZE, total_chunks)}...")
        db.add_documents(batch)

    print(f"Successfully created vector store for {repo_id}")
    return db

def load_vector_store(repo_id):
    embeddings = get_embeddings()
    persist_dir = os.path.join(VECTORSTORE_DIR, repo_id)

    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
