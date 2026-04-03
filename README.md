# ASK Git

A powerful tool to chat with any GitHub repository using RAG (Retrieval-Augmented Generation) powered by Langchain and Openai.

## 🚀 Getting Started

### 1. Setup Environment
Ensure you have a `.env` file in the root directory with your Gemini API key:
```env
OPENAI_API_KEY=your_api_key_here
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Backend Server
```bash
python main.py
```

### 4. Access the Application
Once the server is running, open your browser and navigate to:
[http://localhost:8000](http://localhost:8000)

## 🛠️ Tech Stack
- **Backend:** FastAPI, Uvicorn
- **Frontend:** React
- **AI/RAG:** LangChain, Openai, Chroma
