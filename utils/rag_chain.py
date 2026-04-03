from utils.config import TOP_K
from utils.vector_store import load_vector_store
from utils.llm import get_llm
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from utils.prompt import prompt

def get_qa_chain(repo_id):
    db = load_vector_store(repo_id)
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K}
    )

    qa_chain = create_stuff_documents_chain(get_llm(), prompt)

    rag_chain = create_retrieval_chain(retriever, qa_chain)

    return rag_chain

def ask_question(query, repo_id, chat_history_dicts=None):
    db = load_vector_store(repo_id)

    docs_and_scores = db.similarity_search_with_score(query, k=TOP_K)
    # Sort by distance (ascending = most similar first)
    docs_and_scores.sort(key=lambda x: x[1])
    
    source_docs = []
    for doc, score in docs_and_scores:
        # Convert distance to similarity score (1 - distance for cosine)
        try:
            dist = float(score)
            doc.metadata["distance"] = dist
            doc.metadata["score"] = max(0, 1 - dist)
        except (ValueError, TypeError):
            doc.metadata["score"] = 0.0
        source_docs.append(doc)

    qa = get_qa_chain(repo_id)
    result = qa.invoke({"input": query})
    answer = result["answer"]

    sources = [doc.metadata.get("source", "Unknown") for doc in source_docs]

    return answer, list(set(sources))
