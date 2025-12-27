# Pinecone RAG System

> **Deployment Platform: Microsoft Azure**

A production-grade Retrieval-Augmented Generation (RAG) system for querying 57 AI/ML technical books with high relevance scores (80-95%).

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   User Query    │────▶│   FastAPI       │────▶│   Pinecone      │
│                 │     │   Backend       │     │   Vector DB     │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
              │ OpenAI   │ │ DeepSeek │ │ Cohere   │
              │ Embed    │ │ LLM      │ │ Rerank   │
              └──────────┘ └──────────┘ └──────────┘
```

## Features

| Feature | Description |
|---------|-------------|
| **Hierarchical Semantic Chunking** | Parent/child chunks with 75th percentile semantic breakpoints |
| **Multi-Query Retrieval** | 5 query variations for better recall |
| **HyDE** | Hypothetical Document Embeddings for improved search |
| **Graph RAG** | Knowledge graph with 37 concepts for query expansion |
| **Hybrid Search** | Vector + BM25 keyword matching |
| **Cohere Reranking** | Final relevance scoring with rerank-english-v3.0 |
| **Exact Match Priority** | Original query weighted 20% higher than variations |

## Tech Stack

- **Vector Database**: Pinecone (16,522 vectors, 1024 dimensions)
- **Embeddings**: OpenAI text-embedding-3-large
- **LLM**: DeepSeek (cost-effective alternative to GPT-4)
- **Reranking**: Cohere rerank-english-v3.0
- **Framework**: LlamaIndex + FastAPI
- **Deployment**: Azure App Service

## Project Structure

```
Pinecone-RAG-System/
├── api.py                 # FastAPI server (main entry point)
├── rag_llamaindex.py      # RAG pipeline with all features
├── knowledge_graph.py     # Graph RAG for concept expansion
├── books_config.yaml      # Namespace/category configuration
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container deployment
├── .env.example           # Environment variables template
└── .gitignore             # Git ignore patterns
```

## Categories (Namespaces)

| ID | Description | Vector Count |
|----|-------------|--------------|
| aws | AWS & Cloud Computing | 6,027 |
| llm | LLM & AI Agents | 5,964 |
| arch | AI Architecture & Design | 2,221 |
| ml | ML Fundamentals | 1,260 |
| python | Python Programming | 702 |
| mlops | MLOps & DevOps | 348 |
| **Total** | **All Categories** | **16,522** |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/query` | POST | Main RAG query endpoint |
| `/namespaces` | GET | List available categories |

### Query Request

```json
POST /query
{
  "question": "What is retrieval augmented generation?",
  "category": "all",
  "top_k": 5,
  "use_rerank": true,
  "use_hybrid": true,
  "use_multi_query": true,
  "use_hyde": true,
  "use_graph": true
}
```

### Query Response

```json
{
  "question": "What is retrieval augmented generation?",
  "response": "RAG is a technique that...",
  "sources": [
    {
      "source": "Building LLMS for Production",
      "page": 45,
      "category": "llm",
      "score": "95.2%"
    }
  ]
}
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/lpalad/AWS-Projects.git
cd AWS-Projects/Pinecone-RAG-System
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Run locally

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

## Azure Deployment

### App Service

```bash
# Create App Service Plan
az appservice plan create \
  --name rag-backend-plan \
  --resource-group YourResourceGroup \
  --location australiaeast \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --name your-rag-api \
  --resource-group YourResourceGroup \
  --plan rag-backend-plan \
  --runtime "PYTHON:3.11"

# Configure environment variables
az webapp config appsettings set \
  --name your-rag-api \
  --resource-group YourResourceGroup \
  --settings \
    PINECONE_API_KEY="your_key" \
    OPENAI_API_KEY="your_key" \
    DEEPSEEK_API_KEY="your_key" \
    COHERE_API_KEY="your_key"

# Deploy
az webapp up --name your-rag-api
```

### Docker

```bash
docker build -t pinecone-rag-system .
docker run -p 8000:8000 --env-file .env pinecone-rag-system
```

## Performance

- **Relevance Scores**: 80-95% for specific technical queries
- **Query Latency**: 3-8 seconds (all features enabled)
- **Cold Start**: ~5-10 seconds

## License

MIT License
