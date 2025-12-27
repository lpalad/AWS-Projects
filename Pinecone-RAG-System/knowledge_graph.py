# Lightweight Knowledge Graph for RAG Enhancement
# Extracts concepts from books and maps relationships for improved retrieval
# No Neo4j required - uses JSON for simplicity

import os
import json
from typing import Dict, List, Set, Optional
from pathlib import Path
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI

load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

GRAPH_FILE = "concept_graph.json"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LLM for concept extraction
llm = OpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

# ============================================================================
# CONCEPT GRAPH SCHEMA
# ============================================================================

"""
Graph Structure:
{
    "concepts": {
        "agent_memory": {
            "aliases": ["memory management", "context retention", "conversational memory"],
            "related_to": ["context_window", "vector_database", "rag"],
            "part_of": ["ai_agents"],
            "enables": ["long_conversations", "personalization"],
            "books": ["Building AI Agents", "Managing Memory for AI Agents"],
            "category": "llm"
        },
        ...
    },
    "relationships": [
        {"from": "agent_memory", "to": "context_window", "type": "limited_by"},
        {"from": "rag", "to": "agent_memory", "type": "enables"},
        ...
    ],
    "book_concepts": {
        "Building AI Agents": ["agent_memory", "tool_use", "planning"],
        ...
    }
}
"""

# ============================================================================
# PREDEFINED CONCEPT TAXONOMY (Domain Knowledge)
# ============================================================================

# Core concepts that appear across your 57 AI/ML books
CONCEPT_TAXONOMY = {
    # LLM & Agents
    "llm": {
        "aliases": ["large language model", "language model", "gpt", "claude", "transformer model"],
        "related_to": ["transformer", "attention", "tokenization", "embedding"],
        "category": "llm"
    },
    "ai_agent": {
        "aliases": ["agent", "autonomous agent", "agentic ai", "ai assistant"],
        "related_to": ["tool_use", "planning", "reasoning", "memory"],
        "category": "llm"
    },
    "agent_memory": {
        "aliases": ["memory", "context retention", "conversation history", "memory management"],
        "related_to": ["context_window", "vector_database", "rag", "short_term_memory", "long_term_memory"],
        "category": "llm"
    },
    "context_window": {
        "aliases": ["context length", "token limit", "max tokens", "context size"],
        "related_to": ["tokenization", "agent_memory", "attention"],
        "category": "llm"
    },
    "tool_use": {
        "aliases": ["function calling", "tool calling", "api calling", "agent tools"],
        "related_to": ["ai_agent", "planning", "mcp"],
        "category": "llm"
    },
    "planning": {
        "aliases": ["task planning", "reasoning", "chain of thought", "step by step"],
        "related_to": ["ai_agent", "tool_use", "reasoning"],
        "category": "llm"
    },
    "rag": {
        "aliases": ["retrieval augmented generation", "retrieval", "knowledge retrieval"],
        "related_to": ["embedding", "vector_database", "chunking", "reranking", "hybrid_search"],
        "category": "llm"
    },
    "embedding": {
        "aliases": ["embeddings", "vector embedding", "text embedding", "semantic embedding"],
        "related_to": ["vector_database", "rag", "similarity_search"],
        "category": "llm"
    },
    "vector_database": {
        "aliases": ["vector db", "vector store", "pinecone", "weaviate", "chromadb"],
        "related_to": ["embedding", "rag", "similarity_search"],
        "category": "llm"
    },
    "prompt_engineering": {
        "aliases": ["prompting", "prompt design", "prompt optimization"],
        "related_to": ["llm", "chain_of_thought", "few_shot"],
        "category": "llm"
    },
    "fine_tuning": {
        "aliases": ["finetuning", "model fine-tuning", "transfer learning", "lora", "qlora"],
        "related_to": ["llm", "training", "peft"],
        "category": "llm"
    },
    "langchain": {
        "aliases": ["lang chain", "langchain framework"],
        "related_to": ["rag", "ai_agent", "llm"],
        "category": "llm"
    },
    "llamaindex": {
        "aliases": ["llama index", "gpt index"],
        "related_to": ["rag", "indexing", "retrieval"],
        "category": "llm"
    },

    # RAG Techniques
    "chunking": {
        "aliases": ["text chunking", "document splitting", "text splitting"],
        "related_to": ["rag", "embedding", "indexing"],
        "category": "llm"
    },
    "reranking": {
        "aliases": ["rerank", "cross-encoder", "cohere rerank"],
        "related_to": ["rag", "retrieval", "relevance"],
        "category": "llm"
    },
    "hybrid_search": {
        "aliases": ["hybrid retrieval", "bm25 + vector", "keyword + semantic"],
        "related_to": ["rag", "bm25", "vector_search"],
        "category": "llm"
    },
    "query_rewriting": {
        "aliases": ["query expansion", "query transformation", "hyde"],
        "related_to": ["rag", "retrieval"],
        "category": "llm"
    },

    # ML Fundamentals
    "transformer": {
        "aliases": ["transformer architecture", "attention mechanism", "self-attention"],
        "related_to": ["llm", "attention", "deep_learning"],
        "category": "ml"
    },
    "deep_learning": {
        "aliases": ["neural network", "dnn", "deep neural network"],
        "related_to": ["machine_learning", "pytorch", "tensorflow"],
        "category": "ml"
    },
    "machine_learning": {
        "aliases": ["ml", "statistical learning", "predictive modeling"],
        "related_to": ["deep_learning", "training", "inference"],
        "category": "ml"
    },
    "pytorch": {
        "aliases": ["torch", "pytorch framework"],
        "related_to": ["deep_learning", "training", "tensor"],
        "category": "ml"
    },
    "training": {
        "aliases": ["model training", "learning", "optimization"],
        "related_to": ["machine_learning", "loss_function", "gradient_descent"],
        "category": "ml"
    },
    "inference": {
        "aliases": ["model inference", "prediction", "serving"],
        "related_to": ["deployment", "latency", "throughput"],
        "category": "ml"
    },

    # MLOps
    "mlops": {
        "aliases": ["ml operations", "machine learning operations"],
        "related_to": ["deployment", "monitoring", "pipeline"],
        "category": "mlops"
    },
    "llmops": {
        "aliases": ["llm operations", "llm deployment"],
        "related_to": ["mlops", "llm", "deployment"],
        "category": "mlops"
    },
    "deployment": {
        "aliases": ["model deployment", "production deployment", "serving"],
        "related_to": ["inference", "mlops", "containerization"],
        "category": "mlops"
    },
    "monitoring": {
        "aliases": ["model monitoring", "observability", "metrics"],
        "related_to": ["mlops", "evaluation", "drift_detection"],
        "category": "mlops"
    },
    "pipeline": {
        "aliases": ["ml pipeline", "data pipeline", "ci/cd"],
        "related_to": ["mlops", "automation", "orchestration"],
        "category": "mlops"
    },

    # AWS
    "aws": {
        "aliases": ["amazon web services", "amazon cloud"],
        "related_to": ["cloud", "sagemaker", "bedrock", "lambda"],
        "category": "aws"
    },
    "sagemaker": {
        "aliases": ["amazon sagemaker", "aws sagemaker"],
        "related_to": ["aws", "training", "deployment", "mlops"],
        "category": "aws"
    },
    "bedrock": {
        "aliases": ["amazon bedrock", "aws bedrock"],
        "related_to": ["aws", "llm", "foundation_model"],
        "category": "aws"
    },
    "lambda": {
        "aliases": ["aws lambda", "serverless function"],
        "related_to": ["aws", "serverless", "deployment"],
        "category": "aws"
    },

    # Architecture
    "system_design": {
        "aliases": ["architecture", "design patterns", "software architecture"],
        "related_to": ["scalability", "performance", "microservices"],
        "category": "arch"
    },
    "scalability": {
        "aliases": ["scaling", "horizontal scaling", "vertical scaling"],
        "related_to": ["system_design", "performance", "load_balancing"],
        "category": "arch"
    },
    "latency": {
        "aliases": ["response time", "delay", "speed"],
        "related_to": ["performance", "optimization", "inference"],
        "category": "arch"
    },

    # Python
    "python": {
        "aliases": ["python programming", "python language"],
        "related_to": ["async", "typing", "decorators"],
        "category": "python"
    },
    "async": {
        "aliases": ["asyncio", "asynchronous", "concurrent"],
        "related_to": ["python", "performance", "concurrency"],
        "category": "python"
    },
}

# Relationship types for the graph
RELATIONSHIP_TYPES = {
    "related_to": "General relationship",
    "part_of": "Hierarchical containment",
    "enables": "Causal enablement",
    "requires": "Prerequisite dependency",
    "similar_to": "Semantic similarity",
    "solves": "Problem-solution",
    "limited_by": "Constraint relationship",
    "alternative_to": "Alternative approaches"
}


# ============================================================================
# GRAPH CLASS
# ============================================================================

class ConceptGraph:
    """Lightweight knowledge graph for concept relationships."""

    def __init__(self, graph_file: str = GRAPH_FILE):
        self.graph_file = Path(graph_file)
        self.concepts: Dict[str, dict] = {}
        self.relationships: List[dict] = []
        self.book_concepts: Dict[str, List[str]] = {}
        self.concept_to_books: Dict[str, List[str]] = {}

        # Load existing graph or initialize with taxonomy
        if self.graph_file.exists():
            self.load()
        else:
            self._initialize_from_taxonomy()

    def _initialize_from_taxonomy(self):
        """Initialize graph with predefined concept taxonomy."""
        for concept_id, data in CONCEPT_TAXONOMY.items():
            self.concepts[concept_id] = {
                "id": concept_id,
                "aliases": data.get("aliases", []),
                "related_to": data.get("related_to", []),
                "category": data.get("category", "general"),
                "books": []
            }

        # Build relationships from taxonomy
        for concept_id, data in CONCEPT_TAXONOMY.items():
            for related in data.get("related_to", []):
                if related in self.concepts:
                    self.relationships.append({
                        "from": concept_id,
                        "to": related,
                        "type": "related_to"
                    })

        self.save()
        print(f"Initialized graph with {len(self.concepts)} concepts")

    def save(self):
        """Save graph to JSON file."""
        data = {
            "concepts": self.concepts,
            "relationships": self.relationships,
            "book_concepts": self.book_concepts,
            "concept_to_books": self.concept_to_books
        }
        with open(self.graph_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self):
        """Load graph from JSON file."""
        with open(self.graph_file, 'r') as f:
            data = json.load(f)
        self.concepts = data.get("concepts", {})
        self.relationships = data.get("relationships", [])
        self.book_concepts = data.get("book_concepts", {})
        self.concept_to_books = data.get("concept_to_books", {})
        print(f"Loaded graph with {len(self.concepts)} concepts, {len(self.book_concepts)} books")

    def find_concept(self, term: str) -> Optional[str]:
        """Find concept ID from term or alias."""
        term_lower = term.lower().strip()

        # Direct match
        if term_lower in self.concepts:
            return term_lower

        # Check aliases
        for concept_id, data in self.concepts.items():
            if term_lower in [a.lower() for a in data.get("aliases", [])]:
                return concept_id
            # Partial match
            if term_lower in concept_id or concept_id in term_lower:
                return concept_id

        return None

    def get_related_concepts(self, concept_id: str, depth: int = 1) -> Set[str]:
        """Get concepts related to given concept up to specified depth."""
        if concept_id not in self.concepts:
            return set()

        related = set()
        visited = {concept_id}
        current_level = {concept_id}

        for _ in range(depth):
            next_level = set()
            for c in current_level:
                # Get directly related from concept data
                if c in self.concepts:
                    for r in self.concepts[c].get("related_to", []):
                        if r not in visited:
                            next_level.add(r)
                            related.add(r)

                # Get from relationships
                for rel in self.relationships:
                    if rel["from"] == c and rel["to"] not in visited:
                        next_level.add(rel["to"])
                        related.add(rel["to"])
                    elif rel["to"] == c and rel["from"] not in visited:
                        next_level.add(rel["from"])
                        related.add(rel["from"])

            visited.update(next_level)
            current_level = next_level

        return related

    def get_concept_aliases(self, concept_id: str) -> List[str]:
        """Get all aliases for a concept."""
        if concept_id not in self.concepts:
            return []
        return self.concepts[concept_id].get("aliases", [])

    def extract_concepts_from_query(self, query: str) -> List[str]:
        """Extract known concepts from a user query."""
        query_lower = query.lower()
        found_concepts = []

        for concept_id, data in self.concepts.items():
            # Check concept ID
            if concept_id.replace("_", " ") in query_lower:
                found_concepts.append(concept_id)
                continue

            # Check aliases
            for alias in data.get("aliases", []):
                if alias.lower() in query_lower:
                    found_concepts.append(concept_id)
                    break

        return list(set(found_concepts))

    def expand_query_with_concepts(self, query: str, max_expansions: int = 10) -> dict:
        """
        Expand query using concept graph relationships.

        This is the KEY function that enhances RAG retrieval by:
        1. Extracting concepts from the query
        2. Finding related concepts in the graph
        3. Adding aliases and related terms to search

        Args:
            query: Original user query
            max_expansions: Maximum number of expansion terms

        Returns:
            Dict with original query, extracted concepts, expansions, and enriched queries
        """
        # Step 1: Extract concepts from query
        found_concepts = self.extract_concepts_from_query(query)

        # Step 2: Get related concepts (1-hop neighbors)
        related_concepts = set()
        for concept in found_concepts:
            related = self.get_related_concepts(concept, depth=1)
            related_concepts.update(related)

        # Step 3: Gather expansion terms (aliases + related concept names)
        expansion_terms = set()

        # Add aliases for found concepts
        for concept in found_concepts:
            aliases = self.get_concept_aliases(concept)
            expansion_terms.update(aliases[:3])  # Top 3 aliases

        # Add related concept names and their top alias
        for concept in list(related_concepts)[:5]:  # Top 5 related
            expansion_terms.add(concept.replace("_", " "))
            aliases = self.get_concept_aliases(concept)
            if aliases:
                expansion_terms.add(aliases[0])

        # Limit expansions
        expansion_list = list(expansion_terms)[:max_expansions]

        # Step 4: Build enriched query suggestions
        enriched_queries = []
        if expansion_list:
            # Query + top expansions
            enriched_queries.append(f"{query} ({', '.join(expansion_list[:5])})")
            # Just expansions for alternate search
            enriched_queries.append(' '.join(expansion_list[:7]))

        return {
            "original_query": query,
            "concepts_found": found_concepts,
            "related_concepts": list(related_concepts),
            "expansion_terms": expansion_list,
            "enriched_queries": enriched_queries,
            "graph_enhanced": len(found_concepts) > 0
        }

    def add_book_concepts(self, book_title: str, concepts: List[str]):
        """Associate concepts with a book."""
        self.book_concepts[book_title] = concepts

        # Update reverse mapping
        for concept in concepts:
            if concept not in self.concept_to_books:
                self.concept_to_books[concept] = []
            if book_title not in self.concept_to_books[concept]:
                self.concept_to_books[concept].append(book_title)

            # Update concept's book list
            if concept in self.concepts:
                if book_title not in self.concepts[concept].get("books", []):
                    if "books" not in self.concepts[concept]:
                        self.concepts[concept]["books"] = []
                    self.concepts[concept]["books"].append(book_title)

        self.save()

    def get_books_for_concept(self, concept_id: str) -> List[str]:
        """Get books that cover a specific concept."""
        return self.concept_to_books.get(concept_id, [])

    def add_relationship(self, from_concept: str, to_concept: str, rel_type: str = "related_to"):
        """Add a new relationship to the graph."""
        # Ensure concepts exist
        for c in [from_concept, to_concept]:
            if c not in self.concepts:
                self.concepts[c] = {
                    "id": c,
                    "aliases": [],
                    "related_to": [],
                    "category": "general",
                    "books": []
                }

        # Add relationship
        rel = {"from": from_concept, "to": to_concept, "type": rel_type}
        if rel not in self.relationships:
            self.relationships.append(rel)
            self.save()


# ============================================================================
# LLM-BASED CONCEPT EXTRACTION
# ============================================================================

def extract_concepts_from_text(text: str, book_title: str = "") -> List[str]:
    """
    Use LLM to extract key concepts from a text chunk.

    This is used during indexing to build book-concept mappings.
    """
    prompt = f"""You are extracting key technical concepts from AI/ML book content.

Text from "{book_title}":
{text[:2000]}

Extract the main technical concepts mentioned. Return ONLY a comma-separated list of concepts.
Focus on: AI techniques, ML algorithms, tools, frameworks, architectures, and methodologies.
Use lowercase, replace spaces with underscores.

Example output: agent_memory, rag, vector_database, fine_tuning

Concepts:"""

    try:
        response = llm.complete(prompt)
        concepts_str = str(response).strip()
        concepts = [c.strip().lower().replace(" ", "_") for c in concepts_str.split(",")]
        return [c for c in concepts if len(c) > 2 and len(c) < 50]
    except Exception as e:
        print(f"Concept extraction failed: {e}")
        return []


def extract_relationships_from_text(text: str) -> List[dict]:
    """
    Use LLM to extract concept relationships from text.
    """
    prompt = f"""Analyze this technical text and extract relationships between concepts.

Text:
{text[:2000]}

Extract relationships in this format (one per line):
concept1 | relationship_type | concept2

Relationship types: related_to, enables, requires, part_of, solves, alternative_to

Example:
rag | enables | agent_memory
context_window | limits | conversation_length
vector_database | enables | semantic_search

Relationships:"""

    try:
        response = llm.complete(prompt)
        lines = str(response).strip().split("\n")
        relationships = []

        for line in lines:
            parts = [p.strip().lower().replace(" ", "_") for p in line.split("|")]
            if len(parts) == 3:
                relationships.append({
                    "from": parts[0],
                    "to": parts[2],
                    "type": parts[1]
                })

        return relationships
    except Exception as e:
        print(f"Relationship extraction failed: {e}")
        return []


# ============================================================================
# MAIN / TESTING
# ============================================================================

if __name__ == "__main__":
    # Initialize or load graph
    graph = ConceptGraph()

    print("\n" + "="*60)
    print("CONCEPT GRAPH TEST")
    print("="*60)

    # Test query expansion
    test_queries = [
        "how to implement continuous learning for AI agents",
        "what is the difference between RAG and fine-tuning",
        "how does agent memory work with context windows",
        "deploy LLM to AWS",
        "PyTorch training optimization"
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print("-"*60)

        result = graph.expand_query_with_concepts(query)

        print(f"Concepts found: {result['concepts_found']}")
        print(f"Related concepts: {result['related_concepts'][:5]}")
        print(f"Expansion terms: {result['expansion_terms']}")
        print(f"Graph enhanced: {result['graph_enhanced']}")

        if result['enriched_queries']:
            print(f"\nEnriched queries:")
            for eq in result['enriched_queries']:
                print(f"  - {eq[:100]}...")
