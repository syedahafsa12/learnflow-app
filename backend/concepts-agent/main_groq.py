from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import logging
import os
from groq import Groq

app = FastAPI(title="Concepts Agent (Groq-Powered)", description="Explains Python concepts with Groq LLM", version="2.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY environment variable not set")

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

class ConceptRequest(BaseModel):
    concept: str
    difficulty_level: str = "intermediate"
    user_context: Dict[str, Any] = {}

class ConceptResponse(BaseModel):
    concept: str
    explanation: str
    examples: List[str]
    common_mistakes: List[str]
    related_concepts: List[str]
    difficulty: str

def generate_concept_explanation(concept: str, difficulty: str) -> Dict[str, Any]:
    """Use Groq to generate a comprehensive concept explanation"""

    system_prompt = f"""You are an expert Python programming tutor. Your role is to explain Python concepts clearly and provide helpful examples.

When explaining a concept, structure your response EXACTLY as follows:

EXPLANATION:
[Provide a clear, {difficulty}-level explanation of the concept in 2-3 sentences]

EXAMPLES:
[Provide 3 Python code examples, each on a new line, showing the concept in action]

COMMON_MISTAKES:
[List 3 common mistakes learners make with this concept, one per line]

RELATED_CONCEPTS:
[List 3-4 related Python concepts that would be good to learn next, comma-separated]

Make sure your examples are practical and runnable Python code with comments."""

    user_prompt = f"Explain the Python concept: '{concept}' at a {difficulty} level."

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1500,
        )

        response_text = chat_completion.choices[0].message.content
        logger.info(f"Groq response received: {len(response_text)} characters")

        # Parse the structured response
        result = {
            "explanation": "",
            "examples": [],
            "common_mistakes": [],
            "related_concepts": []
        }

        current_section = None
        lines = response_text.split('\n')

        for line in lines:
            line = line.strip()

            if line.startswith('EXPLANATION:'):
                current_section = 'explanation'
                continue
            elif line.startswith('EXAMPLES:'):
                current_section = 'examples'
                continue
            elif line.startswith('COMMON_MISTAKES:'):
                current_section = 'common_mistakes'
                continue
            elif line.startswith('RELATED_CONCEPTS:'):
                current_section = 'related_concepts'
                continue

            if current_section == 'explanation' and line:
                result['explanation'] += line + ' '
            elif current_section == 'examples' and line and not line.startswith('-'):
                # Accumulate code examples
                if line.startswith('```python'):
                    continue
                elif line.startswith('```'):
                    continue
                else:
                    result['examples'].append(line)
            elif current_section == 'common_mistakes' and line:
                if line.startswith('-') or line.startswith('•'):
                    result['common_mistakes'].append(line.lstrip('-•').strip())
                elif line and not line.startswith('RELATED'):
                    result['common_mistakes'].append(line)
            elif current_section == 'related_concepts' and line:
                # Split by commas for related concepts
                concepts = [c.strip().lstrip('-•') for c in line.replace(',', ' ').split() if c.strip()]
                result['related_concepts'].extend(concepts)

        # Clean up and validate
        result['explanation'] = result['explanation'].strip()

        # If examples weren't parsed well, extract code blocks
        if len(result['examples']) < 2:
            code_block = ""
            in_code_block = False
            for line in lines:
                if '```python' in line or '```' in line:
                    if in_code_block and code_block:
                        result['examples'].append(code_block.strip())
                        code_block = ""
                    in_code_block = not in_code_block
                elif in_code_block:
                    code_block += line + '\n'
                elif line.strip().startswith('#') or 'def ' in line or 'for ' in line or '=' in line:
                    if not in_code_block:
                        result['examples'].append(line)

        # Ensure we have at least some content
        if not result['explanation']:
            result['explanation'] = f"Here's an explanation of {concept} in Python: " + response_text[:500]

        if len(result['examples']) == 0:
            result['examples'] = [
                f"# Example of {concept}\nprint('See explanation above')"
            ]

        if len(result['common_mistakes']) == 0:
            result['common_mistakes'] = ["Check indentation", "Watch for typos", "Read error messages carefully"]

        if len(result['related_concepts']) == 0:
            result['related_concepts'] = ["Python basics", "Control flow", "Data structures"]

        return result

    except Exception as e:
        logger.error(f"Error calling Groq API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate explanation: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "concepts-agent-groq", "model": "llama-3.3-70b-versatile"}

@app.post("/explain", response_model=ConceptResponse)
async def explain_concept(request: ConceptRequest):
    """
    Explain a Python concept using Groq LLM
    """
    concept = request.concept.strip()
    difficulty = request.difficulty_level.lower()

    logger.info(f"Generating explanation for '{concept}' at {difficulty} level using Groq")

    try:
        result = generate_concept_explanation(concept, difficulty)

        return ConceptResponse(
            concept=concept,
            explanation=result['explanation'],
            examples=result['examples'][:3],  # Limit to 3 examples
            common_mistakes=result['common_mistakes'][:3],  # Limit to 3 mistakes
            related_concepts=result['related_concepts'][:4],  # Limit to 4 related concepts
            difficulty=difficulty
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Concepts Agent - Powered by Groq LLM",
        "model": "llama-3.3-70b-versatile",
        "endpoints": {
            "/explain": "POST - Explain any Python concept",
            "/health": "GET - Health check",
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    logger.info(f"Starting Groq-powered Concepts Agent on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
