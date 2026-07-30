import os
import shutil
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from rag_engine import PersonalRAGEngine

app = FastAPI(
    title="Personal RAG Bot API & Web App",
    description="FastAPI Backend & Web Server for Luvkesh Sharma's Personal RAG Chatbot",
    version="1.0.0"
)

# Enable CORS for frontend web application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine
knowledge_path = os.path.join(os.path.dirname(__file__), "knowledge_base")
rag_engine = PersonalRAGEngine(knowledge_dir=knowledge_path)

# Pydantic Schemas
class ChatRequest(BaseModel):
    question: str
    api_key: Optional[str] = None
    history: Optional[List[Dict[str, str]]] = []

class CustomFactRequest(BaseModel):
    question: str
    answer: str
    category: Optional[str] = "General"

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "knowledge_base_files": len(rag_engine.documents_meta),
        "custom_facts_count": len(rag_engine.custom_facts),
        "vectorstore_ready": len(rag_engine.chunks) > 0
    }

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    result = rag_engine.generate_answer(
        question=req.question.strip(),
        groq_api_key=req.api_key,
        conversation_history=req.history
    )
    return result

@app.get("/api/documents")
def get_documents():
    """List all documents in the knowledge base and chunk stats."""
    return {
        "documents": rag_engine.documents_meta,
        "custom_facts_count": len(rag_engine.custom_facts)
    }

@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload PDF, TXT, or MD document to knowledge base."""
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in [".pdf", ".txt", ".md"]:
        raise HTTPException(status_code=400, detail="Only .pdf, .txt, and .md files are supported.")

    file_path = os.path.join(knowledge_path, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Re-index RAG engine
        rag_engine.build_or_load_vectorstore()
        return {
            "message": f"Successfully uploaded and indexed {filename}",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@app.delete("/api/documents/{filename}")
def delete_document(filename: str):
    """Delete a document from knowledge base."""
    file_path = os.path.join(knowledge_path, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            rag_engine.build_or_load_vectorstore()
            return {"message": f"Successfully deleted {filename}"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="File not found.")

@app.get("/api/facts")
def get_facts():
    """List custom facts/Q&A items."""
    return {"facts": rag_engine.custom_facts}

@app.post("/api/facts")
def add_fact(fact_req: CustomFactRequest):
    """Add a new custom fact/Q&A item."""
    if not fact_req.question.strip() or not fact_req.answer.strip():
        raise HTTPException(status_code=400, detail="Question and answer are required.")
    
    new_fact = rag_engine.add_custom_fact(
        question=fact_req.question.strip(),
        answer=fact_req.answer.strip(),
        category=fact_req.category or "General"
    )
    return {"message": "Fact added successfully", "fact": new_fact}

@app.delete("/api/facts/{fact_id}")
def delete_fact(fact_id: str):
    """Delete a custom fact by ID."""
    success = rag_engine.delete_custom_fact(fact_id)
    if success:
        return {"message": "Fact deleted successfully"}
    raise HTTPException(status_code=404, detail="Fact ID not found.")

# Serve Frontend static assets if built
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

