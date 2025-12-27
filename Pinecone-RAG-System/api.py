# FastAPI Backend for RAG System
# Serves the RAG pipeline as a REST API for React frontend

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Union
import uvicorn

# Import the RAG pipeline
from rag_llamaindex import query_books, NAMESPACES

# ============================================================================
# API SETUP
# ============================================================================

app = FastAPI(
    title="AI Books RAG API",
    description="Production RAG API for querying AI/ML technical books",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React dev server
        "http://localhost:5173",      # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://salesconnect.com.au",  # Production domain
        "https://www.salesconnect.com.au",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    question: str
    category: Optional[str] = "all"
    top_k: Optional[int] = 5
    use_rerank: Optional[bool] = True
    use_hybrid: Optional[bool] = True
    use_query_rewrite: Optional[bool] = True
    use_multi_query: Optional[bool] = True  # Generate multiple query variations
    use_hyde: Optional[bool] = True  # Use HyDE for better embedding match
    use_graph: Optional[bool] = True  # Use knowledge graph for concept expansion

class Source(BaseModel):
    source: str
    page: Union[str, int]
    category: str
    score: Union[str, float]
    text_preview: str

class QueryResponse(BaseModel):
    question: str
    namespace: str
    query_rewritten: bool
    search_query: Optional[str]
    multi_query: Optional[bool] = False
    num_queries: Optional[int] = 1
    hyde_used: Optional[bool] = False
    graph_enhanced: Optional[bool] = False  # Knowledge graph used
    concepts_found: Optional[List[str]] = []  # Concepts detected in query
    hybrid_search: bool
    reranked: bool
    response: str
    sources: List[Source]

class NamespaceInfo(BaseModel):
    id: str
    description: str

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "AI Books RAG API is running",
        "version": "1.0.0"
    }


@app.get("/namespaces", response_model=List[NamespaceInfo])
async def get_namespaces():
    """Get available book categories/namespaces"""
    return [
        {"id": ns, "description": desc}
        for ns, desc in NAMESPACES.items()
    ]


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query the RAG system with a question

    - **question**: Your question about AI/ML topics
    - **category**: Book category to search (aws, llm, mlops, ml, arch, python, or all)
    - **top_k**: Number of sources to return (default: 5)
    - **use_rerank**: Enable Cohere reranking (default: true)
    - **use_hybrid**: Enable hybrid BM25 + vector search (default: true)
    - **use_query_rewrite**: Enable LLM query expansion (default: true)
    - **use_graph**: Enable knowledge graph concept expansion (default: true)
    """
    try:
        # Validate category
        if request.category not in NAMESPACES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category. Choose from: {list(NAMESPACES.keys())}"
            )

        # Call the RAG pipeline with enhanced retrieval
        result = query_books(
            question=request.question,
            namespace=request.category,
            top_k=request.top_k,
            use_rerank=request.use_rerank,
            use_hybrid=request.use_hybrid,
            use_query_rewrite=request.use_query_rewrite,
            use_multi_query=request.use_multi_query,
            use_hyde=request.use_hyde,
            use_graph=request.use_graph
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask")
async def ask_simple(question: str, category: str = "all"):
    """
    Simple query endpoint - just question and optional category

    Example: POST /ask?question=how do I implement RAG&category=llm
    """
    try:
        result = query_books(question=question, namespace=category)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    print("Starting RAG API Server...")
    print("Docs available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
