import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.github_loader import clone_repo, get_repo_id
from utils.file_loader import load_files
from utils.vector_store import create_vector_store
from utils.rag_chain import ask_question
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ASK Git", description="A tool to ask questions about GitHub repositories.")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo_status = {}

class ProcessRequest(BaseModel):
    repo_url: str

class QueryRequest(BaseModel):
    question: str
    repo_id: str

@app.get("/")
async def hello():
    return {"message": "Hello, World!"}

@app.post("/api/process")
async def process_repository(request: ProcessRequest, background_tasks: BackgroundTasks):
    repo_url = request.repo_url
    try:
        repo_id = get_repo_id(repo_url)
        repo_status[repo_id] = "processing"
        
        # Run the heavy processing in the background
        background_tasks.add_task(run_indexing, repo_url, repo_id)
        
        return {"repo_id": repo_id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def run_indexing(repo_url, repo_id):
    try:
        path = clone_repo(repo_url)
        docs = load_files(path)
        if not docs:
            repo_status[repo_id] = "failed: no supported files found"
            return
        
        create_vector_store(docs, repo_id)
        repo_status[repo_id] = "completed"
    except Exception as e:
        print(f"Error indexing {repo_id}: {e}")
        repo_status[repo_id] = f"failed: {str(e)}"

@app.get("/api/status/{repo_id}")
async def get_status(repo_id: str):
    status = repo_status.get(repo_id, "unknown")
    return {"repo_id": repo_id, "status": status}

@app.post("/api/query")
async def query_repository(request: QueryRequest):
    try:
        answer, sources = ask_question(request.question, request.repo_id)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)