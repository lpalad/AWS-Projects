# LlamaIndex RAG Pipeline with Pinecone Namespaces
# Features: Cohere Reranking, Hybrid Search (BM25 + Vector), Query Rewriting,
#           Multi-Query, HyDE, and Knowledge Graph Enhancement
# Production-grade RAG for AI/ML technical books

import os
import cohere
from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from rank_bm25 import BM25Okapi
from collections import defaultdict

# Import Knowledge Graph for concept-based query expansion
try:
    from knowledge_graph import ConceptGraph
    GRAPH_AVAILABLE = True
except ImportError:
    GRAPH_AVAILABLE = False
    print("Warning: Knowledge graph not available")

# ============================================================================
# CONFIGURATION (Load from .env file)
# ============================================================================

# Load environment variables from .env file
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "azure")

# Available namespaces
NAMESPACES = {
    "aws": "AWS & Cloud books",
    "llm": "LLM & AI Agents books",
    "mlops": "MLOps & DevOps books",
    "ml": "ML Fundamentals books",
    "arch": "Architecture & Design books",
    "python": "Python Programming books",
    "all": "Search all books"
}

# ============================================================================
# SETUP
# ============================================================================

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(INDEX_NAME)

# Configure LlamaIndex
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-large",
    dimensions=1024
)

Settings.llm = OpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=500
)

# Initialize Cohere client for reranking
co = cohere.Client(COHERE_API_KEY) if COHERE_API_KEY != "YOUR_COHERE_API_KEY" else None

# Initialize Knowledge Graph (lazy loading)
_concept_graph = None

def get_concept_graph():
    """Lazy-load the concept graph."""
    global _concept_graph
    if _concept_graph is None and GRAPH_AVAILABLE:
        _concept_graph = ConceptGraph()
    return _concept_graph


# ============================================================================
# GRAPH-ENHANCED QUERY EXPANSION
# ============================================================================

def expand_query_with_graph(query: str) -> dict:
    """
    Use knowledge graph to expand query with related concepts.

    This adds domain-specific term expansion beyond what Multi-Query and HyDE provide.
    The graph knows that:
    - "agent memory" is related to "context_window", "vector_database", "rag"
    - "RAG" has aliases like "retrieval augmented generation"
    - "fine-tuning" is related to "LoRA", "QLoRA", "transfer learning"

    Args:
        query: Original user query

    Returns:
        Dict with expansion info and enriched query terms
    """
    graph = get_concept_graph()

    if not graph:
        return {
            "original_query": query,
            "graph_enhanced": False,
            "concepts_found": [],
            "expansion_terms": [],
            "enriched_queries": []
        }

    return graph.expand_query_with_concepts(query, max_expansions=10)

# ============================================================================
# MULTI-QUERY REWRITING (Generate multiple query variations)
# ============================================================================

def generate_multi_queries(query: str, num_queries: int = 4) -> dict:
    """
    Generate multiple query variations to improve retrieval coverage.

    Instead of searching with one query, we generate 3-5 variations that
    capture different phrasings of the same concept. This helps when:
    - User language differs from book language
    - Technical concepts have multiple names
    - Query is ambiguous or could be interpreted differently

    Args:
        query: Original user query
        num_queries: Number of query variations to generate (default 4)

    Returns:
        Dict with original query and list of query variations
    """
    multi_query_prompt = f"""You are a search query expert for a technical AI/ML book knowledge base.
The knowledge base contains books on: AWS, LLMs, AI Agents, MLOps, Machine Learning, Python, and AI Architecture.

Given this user query, generate {num_queries} different search queries that capture the same intent.
Each query should use different terminology, synonyms, or phrasings that might appear in technical books.

Rules:
- Each query should be 5-20 words
- Use different technical terms and synonyms
- Cover different aspects of the question
- Include both formal academic terms and practical implementation terms
- Return ONLY the queries, one per line, numbered 1-{num_queries}

Original query: {query}

Generate {num_queries} search variations:"""

    try:
        response = Settings.llm.complete(multi_query_prompt)
        response_text = str(response).strip()

        # Parse numbered queries from response
        queries = []
        for line in response_text.split('\n'):
            line = line.strip()
            # Remove numbering (1., 2., 1), 2), etc.)
            if line and line[0].isdigit():
                # Remove number and punctuation prefix
                cleaned = line.lstrip('0123456789').lstrip('.').lstrip(')').strip()
                if cleaned and len(cleaned) > 5:
                    queries.append(cleaned)

        # Ensure we have at least the original query
        if not queries:
            queries = [query]

        # Add original query if not similar to any generated
        if not any(query.lower() in q.lower() or q.lower() in query.lower() for q in queries):
            queries.insert(0, query)

        return {
            "original": query,
            "queries": queries[:num_queries + 1],  # Cap at num_queries + original
            "num_variations": len(queries)
        }
    except Exception as e:
        print(f"Multi-query generation failed: {e}")
        return {"original": query, "queries": [query], "num_variations": 1}


def rewrite_query(query: str) -> dict:
    """
    Use LLM to expand vague queries into more specific search terms.
    (Legacy function - kept for backward compatibility)

    This helps when users ask things like:
    - "how do I do that thing with data" -> specific technical terms
    - "ML stuff" -> "machine learning algorithms, model training, feature engineering"

    Args:
        query: Original user query

    Returns:
        Dict with original query, rewritten query, and whether rewriting was used
    """
    # Skip rewriting for already specific queries (heuristic: > 8 words usually specific enough)
    word_count = len(query.split())
    if word_count > 8:
        return {"original": query, "rewritten": query, "was_rewritten": False}

    rewrite_prompt = f"""You are a search query optimizer for a technical AI/ML book knowledge base.
The knowledge base contains books on: AWS, LLMs, AI Agents, MLOps, Machine Learning, Python, and AI Architecture.

Given this user query, rewrite it to be more specific and include relevant technical terms that would match content in technical books.
If the query is already specific, return it unchanged.

Rules:
- Keep the rewritten query concise (under 30 words)
- Add relevant technical synonyms or related terms
- Preserve the user's original intent
- Return ONLY the rewritten query, nothing else

Original query: {query}

Rewritten query:"""

    try:
        response = Settings.llm.complete(rewrite_prompt)
        rewritten = str(response).strip()

        # Validate the rewrite isn't too different or too long
        if len(rewritten) > 200 or len(rewritten) < 5:
            return {"original": query, "rewritten": query, "was_rewritten": False}

        return {
            "original": query,
            "rewritten": rewritten,
            "was_rewritten": rewritten.lower() != query.lower()
        }
    except Exception as e:
        print(f"Query rewriting failed: {e}")
        return {"original": query, "rewritten": query, "was_rewritten": False}


# ============================================================================
# HyDE (Hypothetical Document Embeddings)
# ============================================================================

def generate_hypothetical_document(query: str) -> dict:
    """
    Generate a hypothetical document that would answer the query.

    HyDE (Hypothetical Document Embeddings) works by:
    1. LLM generates a hypothetical passage that would answer the query
    2. We embed this passage instead of the query
    3. The passage uses "book-like" language, matching better against actual book content

    This bridges the gap between how users ask questions and how books explain concepts.

    Args:
        query: Original user query

    Returns:
        Dict with original query and hypothetical document
    """
    hyde_prompt = f"""You are an expert technical author writing about AI, Machine Learning, and Cloud Computing.

Given this question, write a 2-3 paragraph passage that would appear in a technical book answering this question.
Write in a formal, educational style similar to O'Reilly or Manning technical books.
Include specific technical terms, concepts, and implementation details.

Question: {query}

Write a hypothetical book passage that answers this:"""

    try:
        response = Settings.llm.complete(hyde_prompt)
        hypothetical_doc = str(response).strip()

        # Validate the response
        if len(hypothetical_doc) < 50:
            return {"original": query, "hypothetical_doc": query, "hyde_used": False}

        return {
            "original": query,
            "hypothetical_doc": hypothetical_doc,
            "hyde_used": True
        }
    except Exception as e:
        print(f"HyDE generation failed: {e}")
        return {"original": query, "hypothetical_doc": query, "hyde_used": False}


# ============================================================================
# SMART NAMESPACE ROUTING
# ============================================================================

# Keywords that suggest specific namespaces (used to boost relevant namespaces)
NAMESPACE_KEYWORDS = {
    "aws": ["aws", "amazon", "s3", "ec2", "lambda", "sagemaker", "bedrock", "dynamodb",
            "cloudformation", "iam", "vpc", "eks", "ecs", "cloud", "serverless"],
    "llm": ["llm", "agent", "agents", "rag", "retrieval", "langchain", "llamaindex",
            "prompt", "embedding", "transformer", "gpt", "claude", "memory", "context",
            "chat", "conversation", "agentic", "autonomous", "mcp", "tool use"],
    "mlops": ["mlops", "devops", "pipeline", "cicd", "ci/cd", "deployment", "monitoring",
              "gitlab", "kubernetes", "docker", "mlflow", "llmops"],
    "ml": ["machine learning", "deep learning", "pytorch", "tensorflow", "keras",
           "neural network", "training", "model", "sklearn", "scikit", "feature"],
    "arch": ["architecture", "design pattern", "system design", "scalability",
             "microservice", "api design", "performance", "engineering"],
    "python": ["python", "decorator", "generator", "async", "asyncio", "typing",
               "dataclass", "pydantic", "fastapi", "flask"]
}


def detect_namespace_relevance(query: str) -> dict:
    """
    Analyze query to detect which namespaces are most relevant.

    Returns dict of namespace -> relevance_score (0-1)
    Used to weight results when searching across all namespaces.
    """
    query_lower = query.lower()
    scores = {}

    for ns, keywords in NAMESPACE_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in query_lower:
                # Exact match gets higher score
                score += 1
        # Normalize to 0-1 range (cap at 1.0)
        scores[ns] = min(score / 2, 1.0)

    # If no keywords matched, return equal scores
    if all(s == 0 for s in scores.values()):
        return {ns: 0.5 for ns in NAMESPACE_KEYWORDS.keys()}

    return scores


# ============================================================================
# HYBRID SEARCH (BM25 + Vector)
# ============================================================================

def bm25_search(query: str, nodes: list, top_k: int = 10) -> list:
    """
    Perform BM25 keyword search on retrieved nodes.

    BM25 excels at:
    - Exact term matching (acronyms like "RAG", "LLM", "MLOps")
    - Technical jargon and specific terminology
    - Cases where semantic similarity misses exact matches

    Args:
        query: Search query
        nodes: List of nodes to search within
        top_k: Number of top results to return

    Returns:
        List of (node, bm25_score) tuples sorted by score
    """
    if not nodes:
        return []

    # Tokenize documents and query
    tokenized_docs = [node.text.lower().split() for node in nodes]
    tokenized_query = query.lower().split()

    # Create BM25 index
    bm25 = BM25Okapi(tokenized_docs)

    # Get scores for each document
    scores = bm25.get_scores(tokenized_query)

    # Pair nodes with scores and sort
    scored_nodes = [(nodes[i], scores[i]) for i in range(len(nodes))]
    scored_nodes.sort(key=lambda x: x[1], reverse=True)

    return scored_nodes[:top_k]


def hybrid_merge(vector_nodes: list, bm25_results: list, alpha: float = 0.7) -> list:
    """
    Merge vector search and BM25 results using Reciprocal Rank Fusion (RRF).

    RRF is a robust method that combines rankings without needing score normalization.
    Formula: RRF(d) = sum(1 / (k + rank(d))) for each ranking

    Args:
        vector_nodes: Nodes from vector search (already have .score)
        bm25_results: List of (node, bm25_score) from BM25 search
        alpha: Weight for vector search (1-alpha for BM25). Default 0.7 favors vectors.

    Returns:
        Merged and deduplicated list of nodes with combined scores
    """
    k = 60  # RRF constant (standard value)

    # Build score map using node text as key (for deduplication)
    rrf_scores = defaultdict(float)
    node_map = {}

    # Score vector results
    for rank, node in enumerate(vector_nodes):
        key = node.text[:100]  # Use text prefix as unique key
        rrf_scores[key] += alpha * (1 / (k + rank + 1))
        node_map[key] = node

    # Score BM25 results
    for rank, (node, bm25_score) in enumerate(bm25_results):
        key = node.text[:100]
        rrf_scores[key] += (1 - alpha) * (1 / (k + rank + 1))
        if key not in node_map:
            node_map[key] = node

    # Sort by combined RRF score
    sorted_keys = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)

    # Build result list with updated scores
    merged_nodes = []
    for key in sorted_keys:
        node = node_map[key]
        node.score = rrf_scores[key]
        merged_nodes.append(node)

    return merged_nodes


# ============================================================================
# RERANKING FUNCTION
# ============================================================================

def rerank_results(query: str, nodes: list, top_n: int = 5) -> list:
    """
    Rerank retrieved nodes using Cohere's reranker for better relevance

    Args:
        query: The user's question
        nodes: List of retrieved nodes from vector search
        top_n: Number of results to return after reranking

    Returns:
        Reranked list of nodes
    """
    if not co or not nodes:
        return nodes[:top_n]

    # Extract text from nodes for reranking
    documents = [node.text for node in nodes]

    try:
        # Use Cohere rerank
        rerank_response = co.rerank(
            model="rerank-v3.5",
            query=query,
            documents=documents,
            top_n=top_n
        )

        # Reorder nodes based on rerank scores
        reranked_nodes = []
        for result in rerank_response.results:
            node = nodes[result.index]
            # Update score with rerank relevance score
            node.score = result.relevance_score
            reranked_nodes.append(node)

        return reranked_nodes

    except Exception as e:
        print(f"Reranking failed: {e}, using original order")
        return nodes[:top_n]


# ============================================================================
# RAG FUNCTIONS
# ============================================================================

def get_retriever(namespace: str = None, top_k: int = 20):
    """Create a retriever for a specific namespace or all"""

    vector_store = PineconeVectorStore(
        pinecone_index=pinecone_index,
        namespace=namespace  # None or "" searches default namespace
    )

    index = VectorStoreIndex.from_vector_store(vector_store)

    # Return retriever instead of query engine (we'll rerank before synthesis)
    return index.as_retriever(similarity_top_k=top_k)


def query_all_namespaces(query: str, top_k_per_ns: int = 15) -> list:
    """
    Query ALL namespaces with smart prioritization.
    Pinecone doesn't support cross-namespace search, so we query each separately.

    Strategy:
    1. Detect which namespaces are most likely relevant based on query keywords
    2. Fetch MORE results from high-relevance namespaces
    3. Apply a small boost to scores from detected namespaces
    4. Let Cohere reranker make final relevance decisions

    Args:
        query: Search query
        top_k_per_ns: Base results to fetch from each namespace (default 15)

    Returns:
        Combined list of nodes from all namespaces, sorted by boosted score
    """
    all_nodes = []
    # ONLY use properly organized namespaces - skip "" (legacy/default)
    active_namespaces = ["aws", "llm", "mlops", "ml", "arch", "python"]

    # Detect which namespaces are likely relevant
    ns_relevance = detect_namespace_relevance(query)
    detected = [ns for ns, score in ns_relevance.items() if score > 0]

    if detected:
        print(f"  Detected relevance: {', '.join(detected)}")
    print(f"  Searching {len(active_namespaces)} namespaces...")

    for ns in active_namespaces:
        try:
            # Fetch more from namespaces that seem relevant to query
            relevance_score = ns_relevance.get(ns, 0.5)
            # High relevance (>0.5): fetch 25 results, low relevance: fetch 10
            adjusted_top_k = int(top_k_per_ns * (0.5 + relevance_score))

            retriever = get_retriever(namespace=ns, top_k=adjusted_top_k)
            nodes = retriever.retrieve(query)

            # Tag each node with its namespace and apply slight boost for detected namespaces
            for node in nodes:
                if 'namespace' not in node.metadata:
                    node.metadata['namespace'] = ns
                # Small boost (5%) for nodes from detected relevant namespaces
                # This helps but doesn't override reranker judgement
                if relevance_score > 0 and node.score:
                    node.score = node.score * (1 + 0.05 * relevance_score)

            all_nodes.extend(nodes)
        except Exception as e:
            print(f"  Warning: Failed to query namespace '{ns}': {e}")

    # Sort all nodes by their (potentially boosted) score before hybrid/rerank
    all_nodes.sort(key=lambda x: x.score if x.score else 0, reverse=True)

    print(f"  Retrieved {len(all_nodes)} total candidates")
    return all_nodes


def query_books(
    question: str,
    namespace: str = "all",
    top_k: int = 5,
    use_rerank: bool = True,
    use_hybrid: bool = True,
    use_query_rewrite: bool = True,
    use_multi_query: bool = True,
    use_hyde: bool = True,
    use_graph: bool = True,
    hybrid_alpha: float = 0.7
) -> dict:
    """
    Query the book knowledge base with production-grade retrieval.

    Enhanced Pipeline:
    0. Graph Expansion: Use knowledge graph to find related concepts
    1. Multi-Query: Generate 4 query variations to cast wider net
    2. HyDE: Generate hypothetical answer for better embedding match
    3. Hybrid Search: Combine BM25 + Vector for each query
    4. Deduplicate & Merge: Combine results from all queries
    5. Rerank: Cohere reranker picks the best matches
    6. Generate: LLM synthesizes final answer

    Args:
        question: Your question
        namespace: Which category to search (aws, llm, mlops, ml, arch, or all)
        top_k: Number of relevant chunks to return
        use_rerank: Whether to use Cohere reranking (default True)
        use_hybrid: Whether to use hybrid search (BM25 + vector) (default True)
        use_query_rewrite: Whether to rewrite vague queries (default True)
        use_multi_query: Whether to generate multiple query variations (default True)
        use_hyde: Whether to use HyDE for embedding (default True)
        use_graph: Whether to use knowledge graph for concept expansion (default True)
        hybrid_alpha: Weight for vector search in hybrid (0-1, default 0.7)

    Returns:
        Dict with response, sources, and metadata
    """
    # Step 0: Knowledge Graph Expansion (find related concepts)
    graph_info = {"graph_enhanced": False, "concepts_found": [], "expansion_terms": [], "enriched_queries": []}
    if use_graph and GRAPH_AVAILABLE:
        graph_info = expand_query_with_graph(question)
        if graph_info["graph_enhanced"]:
            print(f"Query: {question}")
            print(f"Graph: Found concepts {graph_info['concepts_found']}")
            print(f"Graph: Related terms: {graph_info['expansion_terms'][:5]}")

    # Step 1: Generate multiple query variations
    multi_query_info = {"original": question, "queries": [question], "num_variations": 1}
    if use_multi_query:
        multi_query_info = generate_multi_queries(question, num_queries=4)
        print(f"Query: {question}")
        print(f"Generated {multi_query_info['num_variations']} query variations:")
        for i, q in enumerate(multi_query_info['queries'][:3], 1):  # Show first 3
            print(f"  {i}. {q[:80]}{'...' if len(q) > 80 else ''}")
        if len(multi_query_info['queries']) > 3:
            print(f"  ... and {len(multi_query_info['queries']) - 3} more")
    else:
        print(f"Query: {question}")

    # Step 2: Generate HyDE document for embedding
    hyde_info = {"original": question, "hypothetical_doc": question, "hyde_used": False}
    if use_hyde:
        hyde_info = generate_hypothetical_document(question)
        if hyde_info["hyde_used"]:
            print(f"HyDE: Generated hypothetical document ({len(hyde_info['hypothetical_doc'])} chars)")

    # Legacy query rewrite (still useful as fallback)
    query_info = {"original": question, "rewritten": question, "was_rewritten": False}
    if use_query_rewrite and not use_multi_query:
        query_info = rewrite_query(question)
        if query_info["was_rewritten"]:
            print(f"Rewritten: {query_info['rewritten']}")

    # Build list of all queries to search with
    search_queries = []
    if use_multi_query:
        search_queries.extend(multi_query_info['queries'])
    else:
        search_queries.append(query_info.get("rewritten", question))

    # Add HyDE document as an additional search query (truncated for embedding)
    if use_hyde and hyde_info["hyde_used"]:
        # Use first 500 chars of hypothetical doc for embedding
        search_queries.append(hyde_info["hypothetical_doc"][:500])

    # Add Graph-enriched queries (concept expansions)
    if graph_info["graph_enhanced"] and graph_info["enriched_queries"]:
        search_queries.extend(graph_info["enriched_queries"])

    print(f"Searching: {NAMESPACES.get(namespace, namespace)} with {len(search_queries)} queries")

    features = []
    if graph_info["graph_enhanced"]:
        features.append("Graph")
    if use_multi_query:
        features.append("Multi-Query")
    if use_hyde:
        features.append("HyDE")
    if use_hybrid:
        features.append("Hybrid Search")
    if use_rerank and co:
        features.append("Cohere Rerank")
    if use_query_rewrite and not use_multi_query:
        features.append("Query Rewrite")
    print(f"Features: {', '.join(features) if features else 'Basic'}")
    print("-" * 40)

    # Step 3: Multi-Query Retrieval
    # Search with each query variation and combine results
    # IMPORTANT: Original query gets higher weight than variations
    all_retrieved_nodes = []
    seen_texts = set()  # For deduplication
    original_query = question  # Keep original for reranking

    for query_idx, search_query in enumerate(search_queries):
        # First query is always the original - give it higher weight
        is_original_query = (query_idx == 0)

        # Determine fetch count based on settings
        if namespace == "all":
            fetch_per_ns = 15  # Fetch less per query since we have multiple queries
        else:
            fetch_count = 20 if (use_hybrid or use_rerank) else top_k

        # Query all namespaces or specific namespace
        if namespace == "all":
            vector_nodes = query_all_namespaces(search_query, top_k_per_ns=fetch_per_ns)
        else:
            retriever = get_retriever(namespace=namespace, top_k=fetch_count)
            vector_nodes = retriever.retrieve(search_query)

        # Hybrid Search (combine vector + BM25) for this query
        if use_hybrid and vector_nodes:
            bm25_top_k = 30 if namespace == "all" else 15
            bm25_results = bm25_search(search_query, vector_nodes, top_k=bm25_top_k)
            query_nodes = hybrid_merge(vector_nodes, bm25_results, alpha=hybrid_alpha)
        else:
            query_nodes = vector_nodes

        # Add unique nodes to combined results
        # Boost scores for results from original query
        for node in query_nodes:
            text_key = node.text[:150]  # Use text prefix for dedup
            if text_key not in seen_texts:
                seen_texts.add(text_key)
                # Boost original query results by 20% to prioritize exact matches
                if is_original_query and node.score is not None:
                    node.score = node.score * 1.2
                all_retrieved_nodes.append(node)

    print(f"  Combined: {len(all_retrieved_nodes)} unique chunks from {len(search_queries)} queries")

    # Sort combined results by score
    nodes = sorted(all_retrieved_nodes, key=lambda x: x.score if x.score else 0, reverse=True)

    # Step 4: Rerank the merged results
    # CRITICAL: Use ORIGINAL question for reranking, not query variations
    # This ensures Cohere scores relevance to what the user actually asked
    if use_rerank and co:
        # Reranker can handle up to 1000 docs, but more = slower
        # Use top 50 candidates for all-namespace, 30 for specific
        rerank_candidates = min(len(nodes), 50 if namespace == "all" else 30)
        nodes_to_rerank = nodes[:rerank_candidates]
        # Use original_query (user's actual question) for reranking
        nodes = rerank_results(original_query, nodes_to_rerank, top_n=top_k)
    else:
        nodes = nodes[:top_k]

    # Build context from reranked nodes
    context_str = "\n\n".join([
        f"[Source: {n.metadata.get('source', 'Unknown')}, Page {n.metadata.get('page', 'N/A')}]\n{n.text}"
        for n in nodes
    ])

    # Generate response using LLM
    prompt = f"""Based on the following context from technical books, answer the question.
Include citations [Source: Book, Page X] when referencing specific information.

Context:
{context_str}

Question: {question}

Answer:"""

    response = Settings.llm.complete(prompt)

    # Extract source information
    sources = []
    for node in nodes:
        metadata = node.metadata
        # Cohere reranker scores are 0-1, display as percentage
        # Note: If reranking was used, node.score contains the Cohere relevance score
        if node.score is not None:
            if node.score <= 1.0:
                # Cohere reranker score (0-1 range)
                score_display = f"{node.score * 100:.1f}%"
            else:
                # Raw score from somewhere else
                score_display = f"{node.score:.2f}"
        else:
            score_display = "N/A"

        sources.append({
            "source": metadata.get("source", "Unknown"),
            "page": metadata.get("page", "N/A"),
            "category": metadata.get("namespace", metadata.get("category", "N/A")),
            "score": score_display,
            "text_preview": node.text[:200] + "..."
        })

    return {
        "question": question,
        "namespace": namespace,
        "query_rewritten": query_info["was_rewritten"] or use_multi_query,
        "search_query": multi_query_info['queries'][0] if use_multi_query else (query_info["rewritten"] if query_info["was_rewritten"] else None),
        "multi_query": use_multi_query,
        "num_queries": len(search_queries),
        "hyde_used": hyde_info.get("hyde_used", False),
        "graph_enhanced": graph_info.get("graph_enhanced", False),
        "concepts_found": graph_info.get("concepts_found", []),
        "hybrid_search": use_hybrid,
        "reranked": use_rerank and co is not None,
        "response": str(response),
        "sources": sources
    }


def print_result(result: dict):
    """Pretty print query result"""
    print("\n" + "=" * 60)

    # Show pipeline status
    features_used = []
    if result.get("query_rewritten"):
        features_used.append("Query Rewrite")
    if result.get("hybrid_search"):
        features_used.append("Hybrid")
    if result.get("reranked"):
        features_used.append("Reranked")

    print(f"RESPONSE ({', '.join(features_used) if features_used else 'Basic'}):")
    if result.get("search_query"):
        print(f"Searched: \"{result['search_query']}\"")
    print("=" * 60)
    print(result["response"])

    print("\n" + "-" * 60)
    print("SOURCES:")
    print("-" * 60)
    for i, src in enumerate(result["sources"], 1):
        print(f"\n{i}. {src['source']}")
        print(f"   Page: {src['page']} | Category: {src['category']} | Relevance: {src['score']}")


def ask(question: str, category: str = "all"):
    """Quick helper to ask a question"""
    result = query_books(question, namespace=category)
    print_result(result)
    return result


# ============================================================================
# INTERACTIVE MODE
# ============================================================================

def interactive():
    """Interactive Q&A mode"""
    print("\n" + "=" * 60)
    print("INTERACTIVE RAG MODE")
    print("=" * 60)
    print("\nAvailable categories:")
    for ns, desc in NAMESPACES.items():
        print(f"  {ns}: {desc}")

    print("\nCommands:")
    print("  Type your question to search all books")
    print("  Use 'aws: question' to search specific category")
    print("  Type 'quit' to exit")
    print("-" * 60)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not user_input:
            continue

        # Check for category prefix
        namespace = "all"
        question = user_input

        for ns in NAMESPACES.keys():
            if user_input.lower().startswith(f"{ns}:"):
                namespace = ns
                question = user_input[len(ns)+1:].strip()
                break

        result = query_books(question, namespace=namespace)
        print_result(result)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Example queries
    print("Testing Production RAG Pipeline...")
    print("Features: Query Rewrite + Hybrid Search + Cohere Rerank")
    print()

    # Test with agent memory question in LLM category
    result = ask("how do we implement memory to agent AI in e-commerce store", category="llm")
