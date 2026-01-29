from fastapi import FastAPI
from pydantic import BaseModel
import logging
import httpx
from typing import Dict, Any, Optional
from groq import Groq

app = FastAPI(title="Triage Agent", version="1.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Groq client
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    # Try to read from environment file if available
    try:
        import dotenv
        dotenv.load_dotenv()
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    except ImportError:
        pass  # dotenv not available, continue without it

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY environment variable not set")

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

class TriageRequest(BaseModel):
    query: str
    user_id: str
    context: Dict[str, Any] = {}

class TriageResponse(BaseModel):
    agent: str
    response: Any
    route_reason: str

# Service endpoints mapping
SERVICE_ENDPOINTS = {
    'concepts': 'http://localhost:8000/explain',
    'code-review': 'http://localhost:8001/review',  # Will be implemented later
    'debug': 'http://localhost:8000/debug',  # Will be implemented later
    'exercise': 'http://localhost:8002/generate',
    'progress': 'http://localhost:8003/progress'
}

def determine_agent(query: str) -> tuple[str, str]:
    """Determine which agent should handle the query"""
    query_lower = query.lower()

    # Check if query is related to Python programming
    python_keywords = ['python', 'code', 'programming', 'function', 'loop', 'variable', 'list', 'dict', 'dictionary',
                       'class', 'method', 'module', 'import', 'string', 'integer', 'float', 'boolean', 'if', 'else',
                       'elif', 'for', 'while', 'def', 'class', 'object', 'method', 'attribute', 'parameter', 'argument']

    is_python_related = any(keyword in query_lower for keyword in python_keywords)

    # Concept explanation requests (only if Python-related)
    if is_python_related and any(word in query_lower for word in ['what is', 'explain', 'how does', 'concept', 'difference between', 'loops', 'functions', 'variables', 'lists', 'conditionals']):
        return 'concepts', 'Query is asking for Python concept explanation'

    # Exercise/quiz requests (only if Python-related)
    elif is_python_related and any(word in query_lower for word in ['practice', 'exercise', 'quiz', 'test', 'problem', 'challenge', 'give me']):
        return 'exercise', 'Query is requesting Python practice problems'

    # Progress tracking
    elif any(word in query_lower for word in ['progress', 'how am i doing', 'stats', 'track', 'mastery', 'learned']):
        return 'progress', 'Query is about progress tracking'

    # General Python questions
    elif is_python_related and any(word in query_lower for word in ['what is', 'explain', 'how does', 'what are', 'tell me about']):
        return 'concepts', 'General Python question routed to concepts agent'

    # Default to groq for non-Python related questions
    else:
        return 'groq', 'Using Groq for general questions and non-Python topics'


def get_groq_response(query: str) -> Dict[str, Any]:
    """Get response from Groq for general questions"""
    try:
        # Check if groq_client is initialized
        if not groq_client:
            logger.error("Groq client not initialized - API key missing")
            return {
                "message": f"Sorry, I'm having trouble processing your request right now. Could you try rephrasing your question? Original query: {query}",
                "source": "fallback",
                "error": "Groq API key not configured"
            }

        system_prompt = """You are an expert Python programming tutor. Provide helpful, accurate, and educational responses to students learning Python.
        If the question is about Python programming, give detailed explanations with code examples.
        If the question is general, provide the best possible answer."""

        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            model="llama-3.1-8b-instant",  # Updated to current supported model
            temperature=0.7,
            max_tokens=1000
        )

        return {
            "message": response.choices[0].message.content,
            "source": "groq",
            "model": "llama-3.1-8b-instant"  # Updated to current supported model
        }
    except Exception as e:
        logger.error(f"Error calling Groq API: {e}")
        return {
            "message": f"Sorry, I'm having trouble processing your request right now. Could you try rephrasing your question? Original query: {query}",
            "source": "fallback",
            "error": str(e)
        }

@app.post("/triage", response_model=TriageResponse)
async def triage_request(request: TriageRequest):
    """Route the request to the appropriate agent"""
    logger.info(f"Triage request: {request.query}")

    # Determine which agent to route to
    agent, reason = determine_agent(request.query)
    logger.info(f"Routing to agent: {agent}, reason: {reason}")

    # Prepare request data based on agent type
    if agent == 'concepts':
        service_url = 'http://localhost:8000/explain'
        payload = {
            "concept": request.query,
            "difficulty_level": "beginner",
            "user_context": {
                "user_id": request.user_id,
                **request.context
            }
        }

        # Make request to concepts agent
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(service_url, json=payload)
                response.raise_for_status()
                result = response.json()

                return TriageResponse(
                    agent=agent,
                    response=result,
                    route_reason=reason
                )
            except httpx.RequestError as exc:
                logger.error(f"Error contacting concepts agent: {exc}")
                return TriageResponse(
                    agent=agent,
                    response={"error": f"Could not contact concepts agent: {str(exc)}"},
                    route_reason=reason
                )
            except httpx.HTTPStatusError as exc:
                logger.error(f"HTTP error from concepts agent: {exc}")
                return TriageResponse(
                    agent=agent,
                    response={"error": f"Concepts agent returned error: {exc.response.status_code}"},
                    route_reason=reason
                )

    elif agent == 'exercise':
        service_url = 'http://localhost:8002/generate'
        payload = {
            "topic": request.query,
            "difficulty": "beginner",
            "user_context": {
                "user_id": request.user_id,
                **request.context
            }
        }

        # Make request to exercise agent
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(service_url, json=payload)
                response.raise_for_status()
                result = response.json()

                return TriageResponse(
                    agent=agent,
                    response=result,
                    route_reason=reason
                )
            except httpx.RequestError as exc:
                logger.error(f"Error contacting exercise agent: {exc}")
                return TriageResponse(
                    agent=agent,
                    response={"error": f"Could not contact exercise agent: {str(exc)}"},
                    route_reason=reason
                )
            except httpx.HTTPStatusError as exc:
                logger.error(f"HTTP error from exercise agent: {exc}")
                return TriageResponse(
                    agent=agent,
                    response={"error": f"Exercise agent returned error: {exc.response.status_code}"},
                    route_reason=reason
                )

    elif agent == 'progress':
        # For progress, we'll return a mock response since we need the user ID
        return TriageResponse(
            agent=agent,
            response={
                "message": f"Progress for user {request.user_id}",
                "overall_mastery": 0.6,
                "recent_activities": ["Completed loops tutorial", "Solved 3 exercises", "Reviewed functions"],
                "recommended_next": "Practice with functions"
            },
            route_reason=reason
        )

    elif agent == 'groq':
        # Use Groq for general questions
        groq_result = get_groq_response(request.query)

        return TriageResponse(
            agent=agent,
            response=groq_result,
            route_reason=reason
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "triage-agent"}

@app.get("/")
async def root():
    return {
        "message": "Triage Agent - Routes queries to appropriate AI tutors",
        "endpoints": {
            "/triage": "POST - Route query to appropriate agent",
            "/health": "GET - Health check"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
