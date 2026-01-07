<p align="center">
  <img src="https://img.shields.io/badge/Pinecone_RAG-No--Hallucination_AI._95%25_Retrieval_Accuracy.-32CD32?style=for-the-badge" alt="Pinecone RAG"/>
</p>

<h3 align="center">Production-Grade Retrieval-Augmented Generation | Deployed on Microsoft Azure</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Pinecone-000000?style=for-the-badge&logo=pinecone&logoColor=white" alt="Pinecone"/>
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI"/>
  <img src="https://img.shields.io/badge/Cohere-39594D?style=for-the-badge&logo=cohere&logoColor=white" alt="Cohere"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Microsoft_Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" alt="Azure"/>
</p>

---

> "Most RAG demos fail in production because they hallucinate or lack context. I built this system to index 57 technical AI/ML books with a logical architecture that prioritises factual truth over creative guessing."

---

<h2 align="center">Executive Summary: Engineering Profit through Data Rigor</h2>

AI is a liability if it provides incorrect answers. In technical sectors, "hallucinations" lead to expensive mistakes. With over a decade in the IT field and an MBA, I understand that AI must be an asset, not a risk.

My RAG architecture is defined by three logical pillars:

**Certainty:** I use Hierarchical Semantic Chunking and Cohere Reranking to ensure the most relevant technical context is always found.

**Efficiency:** I implemented Hybrid Search (Vector + BM25). We don't just search for "concepts"; we search for specific technical keywords to guarantee precision.

**Fiscal Discipline:** I utilise DeepSeek as a cost-effective LLM alternative to GPT-4, delivering elite performance at a fraction of the token cost.

---

<h2 align="center">Why This Architecture Wins (The Logic)</h2>

| The Feature | The Logical Justification | The Result |
|-------------|---------------------------|------------|
| **Graph RAG** | Uses a Knowledge Graph of 37 concepts for query expansion. | Contextual Awareness. The AI understands how topics relate. |
| **HyDE & Multi-Query** | Generates 5 variations of the query to broaden search recall. | Higher Recall. Finds the answer even if the user asks the wrong way. |
| **Exact Match Priority** | Weights the original user query 20% higher than AI variations. | User Intent. Prevents the AI from "drifting" away from the actual question. |
| **Azure Deployment** | Built for Enterprise-grade uptime in the australiaeast region. | Reliability. Low latency for Australian and NZ business operations. |

---

<h2 align="center">Project Structure: Tools of Precision</h2>

```
Pinecone-RAG-System/
├── api.py                 # FastAPI server (High-performance entry point)
├── rag_llamaindex.py      # Core RAG pipeline (Logic & Reranking)
├── knowledge_graph.py     # Graph RAG engine (Concept expansion)
├── books_config.yaml      # Namespace/Category logic
├── requirements.txt       # Production dependencies
└── Dockerfile             # Containerisation for Azure App Service
```

---

<h2 align="center">Usage & Implementation</h2>

### 1. Technical Setup

**Clone and Configure:**

```bash
git clone https://github.com/lpalad/AWS-Projects.git
cd AWS-Projects/Pinecone-RAG-System
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Define PINECONE, OPENAI, DEEPSEEK, and COHERE keys
```

**Execution:**

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### 2. Query Request (The Logic of Ingestion)

To get the highest accuracy, the system accepts a JSON payload with all advanced features enabled by default:

```
POST /query
```

```json
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

### 3. Query Response (The Logic of Evidence)

The system doesn't just answer; it provides Source Attribution with page numbers and confidence scores.

```json
{
  "question": "What is retrieval augmented generation?",
  "response": "RAG is a technique that...",
  "sources": [
    {
      "source": "Building LLMS for Production",
      "page": 45,
      "score": "95.2%"
    }
  ]
}
```

---

<h2 align="center">Azure Deployment: Enterprise Hosting</h2>

I deploy this using Azure App Service for high availability and simplified scaling.

```bash
# 1. Create App Service Plan in Australia East
az appservice plan create --name rag-backend-plan --resource-group MyGroup --location australiaeast --sku B1 --is-linux

# 2. Deploy Containerised API
az webapp create --name your-rag-api --resource-group MyGroup --plan rag-backend-plan --runtime "PYTHON:3.11"

# 3. Secure Environment (No hardcoded keys)
az webapp config appsettings set --name your-rag-api --resource-group MyGroup --settings PINECONE_API_KEY="key" OPENAI_API_KEY="key"
```

---

<h2 align="center">Performance Metrics</h2>

- **Relevance Scores:** 80-95% on complex technical queries.
- **Latency:** 3-8 seconds (full multi-query and reranking enabled).
- **Storage:** 16,522 vectors across 6 categorised namespaces (AWS, LLM, MLOps, etc.).

---

<h2 align="center">About Me: Leonard S Palad</h2>

**MBA | Master of AI (In Progress)**

I build systems that work. With over a decade in the IT field, I bridge the gap between technical rigor and business outcomes. I document everything, I track everything, and I build to survive production.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/leonardspalad/)
[![AI Portfolio](https://img.shields.io/badge/AI_Portfolio-View_Projects-4285F4?style=for-the-badge)](https://salesconnect.com.au/aip.html)
[![Blog](https://img.shields.io/badge/Blog-Cloud_Hermit-FF5722?style=for-the-badge)](https://www.cloudhermit.com.au/)

---

## License

MIT License
