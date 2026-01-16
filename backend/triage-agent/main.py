from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
from typing import Dict, Any
import asyncio

# Initialize FastAPI app
app = FastAPI(title="Triage Agent", description="Routes student queries to specialist agents", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    query: str
    user_id: str
    context: Dict[str, Any] = {}

class QueryResponse(BaseModel):
    routed_to: str
    confidence: float
    explanation: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "triage-agent"}

@app.post("/triage", response_model=QueryResponse)
async def triage_query(request: QueryRequest):
    """
    Analyze student query and route to appropriate specialist agent

    Categories:
    - concepts: Conceptual questions about Python
    - code_review: Code quality and style review
    - debug: Error troubleshooting
    - exercise: Exercise and challenge assistance
    - progress: Progress tracking and assessment
    """
    query_lower = request.query.lower()

    # Define routing logic based on query content
    routing_rules = [
        # Concept-related queries
        (["what is", "how does", "explain", "difference between", "concept of", "mean", "definition", "describe", "understand"],
         "concepts", 0.9),

        # Debug-related queries
        (["error", "not working", "bug", "exception", "traceback", "failed", "doesn't work", "problem", "fix", "troubleshoot"],
         "debug", 0.95),

        # Code review-related queries
        (["review", "check", "style", "improve", "optimize", "best practice", "pep 8", "refactor", "better way"],
         "code_review", 0.85),

        # Exercise-related queries
        (["exercise", "challenge", "quiz", "assignment", "homework", "practice", "problem to solve"],
         "exercise", 0.8),

        # Progress-related queries
        (["progress", "how am I doing", "track", "mastery", "score", "level", "completed"],
         "progress", 0.8)
    ]

    # Analyze query against routing rules
    best_match = ("unknown", 0.0, "Could not determine appropriate agent for this query")

    for keywords, agent, base_confidence in routing_rules:
        keyword_matches = sum(1 for keyword in keywords if keyword in query_lower)
        if keyword_matches > 0:
            # Calculate confidence based on keyword matches and base confidence
            confidence = min(base_confidence + (keyword_matches * 0.05), 1.0)
            if confidence > best_match[1]:
                best_match = (agent, confidence, f"Query matched keywords for {agent} agent")

    logger.info(f"Triage result: {best_match[0]} with confidence {best_match[1]} for query: {request.query[:50]}...")

    return QueryResponse(
        routed_to=best_match[0],
        confidence=best_match[1],
        explanation=best_match[2]
    )

@app.post("/triage/batch")
async def triage_batch(queries: list[QueryRequest]):
    """Process multiple queries in batch"""
    results = []
    for query_request in queries:
        result = await triage_query(query_request)
        results.append(result)

    return results

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)