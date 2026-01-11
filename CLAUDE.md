# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

AWS-Projects is a collection of 12 production-ready AWS solutions. The primary project is **Pinecone-RAG-System**, a production-grade RAG system deployed on Microsoft Azure that indexes 57 AI/ML technical books with 80-95% retrieval accuracy.

## Build & Run Commands

### Pinecone-RAG-System (Primary Project)

```bash
# Setup
cd Pinecone-RAG-System
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Fill in API keys

# Run locally
uvicorn api:app --host 0.0.0.0 --port 8000

# Run with auto-reload (development)
uvicorn api:app --reload

# Docker
docker build -t rag-api .
docker run -p 8000:8000 --env-file .env rag-api

# Test query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "what is RAG?", "category": "llm"}'
```

### Terraform Projects

```bash
cd Terraform
terraform init
terraform plan
terraform apply
```

## Architecture: Pinecone-RAG-System

### Data Flow
```
User Query → api.py (FastAPI) → rag_llamaindex.py (Pipeline) → Response
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
           knowledge_graph.py     Pinecone API         Cohere API
           (concept expansion)    (vector search)      (reranking)
```

### Core Files

| File | Purpose |
|------|---------|
| `api.py` | FastAPI REST endpoints: `/query`, `/namespaces`, `/ask` |
| `rag_llamaindex.py` | RAG pipeline: multi-query, HyDE, hybrid search, reranking |
| `knowledge_graph.py` | 37-concept graph for query expansion (local JSON, no API) |
| `books_config.yaml` | Book-to-namespace mappings (6 categories, 57 books) |

### RAG Pipeline Steps

1. **Graph Expansion** - Find related concepts from knowledge graph
2. **Multi-Query** - Generate 5 query variations via OpenAI
3. **HyDE** - Create hypothetical document for better embedding match
4. **Vector Search** - Query Pinecone (16,522 vectors, 1024 dimensions)
5. **Hybrid Merge** - Combine BM25 keyword + vector results (RRF)
6. **Rerank** - Cohere cross-encoder scores top 50 → returns top 5
7. **Generate** - OpenAI synthesizes answer with source citations

### Namespaces (Pinecone)

- `aws` - AWS & Cloud books (6,027 vectors)
- `llm` - LLM & AI Agents books (5,964 vectors)
- `arch` - Architecture books (2,221 vectors)
- `ml` - ML Fundamentals (1,260 vectors)
- `python` - Python books (702 vectors)
- `mlops` - MLOps books (348 vectors)

## Environment Variables

Required for Pinecone-RAG-System (`.env` file):

```
PINECONE_API_KEY=xxx
PINECONE_INDEX_NAME=azure
OPENAI_API_KEY=xxx
COHERE_API_KEY=xxx
DEEPSEEK_API_KEY=xxx  # Optional, cost-effective LLM alternative
```

## API Endpoints

```
GET  /              # Health check
GET  /namespaces    # List available categories
POST /query         # Full RAG query with all options
POST /ask           # Simple query (question + category params)
GET  /docs          # Swagger UI (FastAPI auto-generated)
```

### Query Options

```json
{
  "question": "how do agents use memory?",
  "category": "llm",
  "top_k": 5,
  "use_rerank": true,
  "use_hybrid": true,
  "use_multi_query": true,
  "use_hyde": true,
  "use_graph": true
}
```

## Project Categories

| Category | Projects |
|----------|----------|
| AI/ML | Pinecone-RAG-System, House-Price-Predictor, aws-docs-chatbot |
| Infrastructure | Terraform (ECS Fargate), IoT, aws-multi-region-ha, aws-decoupled-architecture |
| CI/CD | CI-CD, aws-devops-journey |
| Networking | AWS CloudFront with Nginx Reverse Proxy |
| API | AWS API Integration, aws-iot-lambda |

## Deployment

### Azure (Pinecone-RAG-System)

```bash
az appservice plan create --name rag-plan --resource-group MyGroup --location australiaeast --sku B1 --is-linux
az webapp create --name rag-api --resource-group MyGroup --plan rag-plan --runtime "PYTHON:3.11"
az webapp config appsettings set --name rag-api --resource-group MyGroup --settings PINECONE_API_KEY="xxx" OPENAI_API_KEY="xxx"
```

### AWS (Terraform Projects)

```bash
cd Terraform
terraform init && terraform apply
```

## Tech Stack

- **Backend**: FastAPI, Python 3.11, Uvicorn
- **RAG Framework**: LlamaIndex
- **Vector DB**: Pinecone
- **Embeddings**: OpenAI text-embedding-3-large
- **LLM**: GPT-4o-mini (or DeepSeek)
- **Reranking**: Cohere rerank-v3.5
- **Infrastructure**: Terraform, Docker, GitHub Actions
- **Cloud**: AWS (most projects), Azure (RAG system)

---

## Architecture: House-Price-Predictor

End-to-end MLOps pipeline demonstrating ML best practices with experiment tracking, model registry, API serving, and web UI.

### Build & Run Commands

```bash
cd House-Price-Predictor

# Setup
uv venv --python python3.11  # or: python -m venv venv
source .venv/bin/activate
uv pip install -r requirements.txt  # or: pip install -r requirements.txt

# Step 1: Data Processing
python src/data/run_processing.py \
  --input data/raw/house_data.csv \
  --output data/processed/cleaned_house_data.csv

# Step 2: Feature Engineering
python src/features/engineer.py \
  --input data/processed/cleaned_house_data.csv \
  --output data/processed/featured_house_data.csv \
  --preprocessor models/trained/preprocessor.pkl

# Step 3: Start MLflow
cd deployment/mlflow && docker compose up -d
# Access MLflow UI at http://localhost:5555

# Step 4: Train Model
python src/models/train_model.py \
  --config configs/model_config.yaml \
  --data data/processed/featured_house_data.csv \
  --models-dir models \
  --mlflow-tracking-uri http://localhost:5555

# Step 5: Run Full Stack (FastAPI + Streamlit)
docker-compose up -d
# FastAPI: http://localhost:8888
# Streamlit: http://localhost:8501

# Test prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"sqft": 1500, "bedrooms": 3, "bathrooms": 2, "location": "suburban", "year_built": 2000, "condition": "fair"}'
```

### Pipeline Architecture

```
Raw Data → Data Cleaning → Feature Engineering → Model Training → API Serving → Web UI
              │                   │                    │              │           │
     run_processing.py      engineer.py         train_model.py    main.py     app.py
```

### Core Files

| File | Purpose |
|------|---------|
| `src/data/run_processing.py` | Clean data: missing values, outlier removal (IQR) |
| `src/features/engineer.py` | Create features: house_age, price_per_sqft, bed_bath_ratio |
| `src/models/train_model.py` | Train model with MLflow tracking and registry |
| `src/api/main.py` | FastAPI endpoints: `/predict`, `/batch-predict`, `/health` |
| `streamlit_app/app.py` | Interactive web UI for predictions |
| `configs/model_config.yaml` | Model hyperparameters (GradientBoosting) |

### MLflow Integration

- **Experiment Tracking**: All runs logged with metrics (MAE, R²)
- **Model Registry**: Automatic versioning with stage transitions
- **Artifacts**: Models saved as pickle files
- **UI**: http://localhost:5555 (via docker-compose)

### Model Performance

- **Algorithm**: GradientBoostingRegressor
- **R² Score**: 0.9938 (99.38% variance explained)
- **MAE**: $10,779.28

### API Endpoints

```
GET  /health         # {"status": "healthy", "model_loaded": true}
POST /predict        # Single prediction with confidence interval
POST /batch-predict  # Multiple predictions
GET  /docs           # Swagger UI
```

### Request Schema

```json
{
  "sqft": 1500,
  "bedrooms": 3,
  "bathrooms": 2,
  "location": "suburban",  // urban, suburban, rural
  "year_built": 2000,
  "condition": "fair"      // Good, Excellent, Fair
}
```

### CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/mlops-pipeline.yaml`):
1. **Data Processing Job**: Clean and engineer features
2. **Model Training Job**: Train with MLflow, upload artifacts
3. **Build & Publish Job**: Multi-platform Docker images to Docker Hub

### Deployment Options

```bash
# Local with Docker Compose
docker-compose up -d

# Kubernetes
kubectl apply -k deployment/kubernetes/
```
