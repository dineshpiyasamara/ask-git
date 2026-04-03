# GitHub RAG Assistant

A powerful tool to chat with any GitHub repository using RAG (Retrieval-Augmented Generation) powered by Google Gemini.

## 🚀 Getting Started

### 1. Setup Environment
Ensure you have a `.env` file in the root directory with your Gemini API key:
```env
GOOGLE_API_KEY=your_api_key_here
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Backend Server
```bash
python backend.py
```

### 4. Access the Application
Once the server is running, open your browser and navigate to:
[http://localhost:8000](http://localhost:8000)

> [!IMPORTANT]
> **Do not** open `static/index.html` directly from your folders. The application requires a web server to communicate with the backend API. Always access it via `http://localhost:8000`.

## 🛠️ Tech Stack
- **Backend:** FastAPI, Uvicorn
- **Frontend:** HTML, CSS, JavaScript
- **AI/RAG:** LangChain, Google Gemini, FAISS
