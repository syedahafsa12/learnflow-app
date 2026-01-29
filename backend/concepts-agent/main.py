from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import os

app = FastAPI(title="Concepts Agent", description="Explains Python concepts with examples", version="1.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConceptRequest(BaseModel):
    concept: str
    difficulty_level: str = "intermediate"  # beginner, intermediate, advanced
    user_context: Dict[str, Any] = {}

class ConceptResponse(BaseModel):
    concept: str
    explanation: str
    examples: List[str]
    common_mistakes: List[str]
    related_concepts: List[str]
    difficulty: str

# Knowledge base for Python concepts
CONCEPT_DATABASE = {
    "loops": {
        "beginner": {
            "explanation": "Loops in Python allow you to repeat a block of code multiple times. The two main types are 'for' loops (for iterating over a sequence) and 'while' loops (for repeating until a condition is false).",
            "examples": [
                "# For loop example\nfor i in range(5):\n    print(i)  # Prints 0, 1, 2, 3, 4",
                "# While loop example\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1",
                "# Loop through a list\nfruits = ['apple', 'banana', 'cherry']\nfor fruit in fruits:\n    print(fruit)"
            ],
            "common_mistakes": [
                "Off-by-one errors: range(5) gives 0-4, not 1-5",
                "Infinite loops: forgetting to increment counter in while loops",
                "Modifying a list while iterating over it"
            ],
            "related_concepts": ["range() function", "break and continue statements", "list comprehensions", "enumerate()"]
        },
        "intermediate": {
            "explanation": "Loops in Python provide powerful iteration capabilities. For loops work with iterables (lists, strings, ranges), while loops continue until a condition is False. You can control loop flow with break (exit loop) and continue (skip to next iteration). Nested loops allow iteration over multi-dimensional data.",
            "examples": [
                "# Nested loops\nfor i in range(3):\n    for j in range(3):\n        print(f'({i}, {j})', end=' ')\n    print()  # New line after inner loop",
                "# Loop with enumerate\nfor index, value in enumerate(['a', 'b', 'c']):\n    print(f'Index {index}: {value}')",
                "# Loop with break and continue\nfor num in range(10):\n    if num == 3:\n        continue  # Skip 3\n    if num == 7:\n        break  # Stop at 7\n    print(num)"
            ],
            "common_mistakes": [
                "Confusion between range(5) and range(0, 5) - they're the same",
                "Not understanding that 'for' creates a new variable in each iteration",
                "Forgetting that strings and lists are iterable"
            ],
            "related_concepts": ["iterators and generators", "list comprehensions", "while-else construct", "zip() function"]
        }
    },
    "variables": {
        "beginner": {
            "explanation": "Variables in Python are containers that store data values. Unlike some languages, you don't need to declare a variable's type - Python figures it out automatically. You create a variable by assigning a value using the equals sign (=).",
            "examples": [
                "# Creating variables\nname = 'Alice'  # String\nage = 25  # Integer\nheight = 5.6  # Float\nis_student = True  # Boolean",
                "# Variables can change type\nx = 5\nprint(x)  # 5\nx = 'hello'\nprint(x)  # hello",
                "# Multiple assignment\na, b, c = 1, 2, 3\nprint(a, b, c)  # 1 2 3"
            ],
            "common_mistakes": [
                "Using reserved keywords as variable names (like 'class', 'for', 'if')",
                "Starting variable names with numbers (5x is invalid, x5 is valid)",
                "Forgetting that variables are case-sensitive (Name ≠ name)"
            ],
            "related_concepts": ["data types", "type conversion", "constants", "naming conventions"]
        }
    },
    "functions": {
        "beginner": {
            "explanation": "Functions are reusable blocks of code that perform a specific task. They help organize code and avoid repetition. Define a function with 'def', give it a name, specify parameters in parentheses, and indent the code block. Use 'return' to send a value back.",
            "examples": [
                "# Simple function\ndef greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('Alice'))  # Hello, Alice!",
                "# Function with multiple parameters\ndef add(a, b):\n    return a + b\n\nresult = add(5, 3)\nprint(result)  # 8",
                "# Function with default parameter\ndef greet(name='Guest'):\n    return f'Hello, {name}!'\n\nprint(greet())  # Hello, Guest!\nprint(greet('Bob'))  # Hello, Bob!"
            ],
            "common_mistakes": [
                "Forgetting to call the function with parentheses: greet vs greet()",
                "Not returning a value when you need one",
                "Confusing parameters (definition) with arguments (actual values)"
            ],
            "related_concepts": ["return statement", "parameters vs arguments", "scope", "lambda functions"]
        }
    },
    "lists": {
        "beginner": {
            "explanation": "Lists in Python are ordered, mutable collections that can hold items of different types. They're created with square brackets [] and items are separated by commas. Lists are zero-indexed, meaning the first element is at index 0.",
            "examples": [
                "# Creating lists\nfruits = ['apple', 'banana', 'cherry']\nnumbers = [1, 2, 3, 4, 5]\nmixed = [1, 'hello', True, 3.14]",
                "# Accessing elements\nfruits = ['apple', 'banana', 'cherry']\nprint(fruits[0])  # apple\nprint(fruits[-1])  # cherry (last item)",
                "# Modifying lists\nfruits.append('date')  # Add to end\nfruits.insert(1, 'blueberry')  # Insert at position\nfruits.remove('apple')  # Remove specific item\nfruits.pop()  # Remove and return last item"
            ],
            "common_mistakes": [
                "Index out of range errors - trying to access an index that doesn't exist",
                "Forgetting that lists are mutable - changes affect the original",
                "Confusion between append() (adds one item) and extend() (adds multiple)"
            ],
            "related_concepts": ["list slicing", "list comprehensions", "sorting", "tuples"]
        }
    },
    "conditionals": {
        "beginner": {
            "explanation": "Conditional statements (if, elif, else) allow your program to make decisions and execute different code based on conditions. Conditions are expressions that evaluate to True or False. Python uses indentation to define code blocks.",
            "examples": [
                "# Simple if statement\nage = 18\nif age >= 18:\n    print('You are an adult')",
                "# if-else\nage = 15\nif age >= 18:\n    print('You are an adult')\nelse:\n    print('You are a minor')",
                "# if-elif-else\nscore = 85\nif score >= 90:\n    print('Grade: A')\nelif score >= 80:\n    print('Grade: B')\nelif score >= 70:\n    print('Grade: C')\nelse:\n    print('Grade: F')"
            ],
            "common_mistakes": [
                "Using = (assignment) instead of == (comparison)",
                "Forgetting the colon : after the condition",
                "Incorrect indentation - Python is strict about this!"
            ],
            "related_concepts": ["comparison operators", "logical operators (and, or, not)", "boolean values", "truthiness"]
        }
    }
}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "concepts-agent"}

@app.post("/explain", response_model=ConceptResponse)
async def explain_concept(request: ConceptRequest):
    """
    Explain a Python concept with examples and common mistakes
    """
    concept_key = request.concept.lower().strip()
    difficulty = request.difficulty_level.lower()

    logger.info(f"Explaining concept: {concept_key} at {difficulty} level")

    # Find the concept in the database
    concept_data = None

    # Try exact match first
    if concept_key in CONCEPT_DATABASE:
        concept_data = CONCEPT_DATABASE[concept_key].get(difficulty)
        # Fallback to beginner if requested difficulty not available
        if not concept_data:
            concept_data = CONCEPT_DATABASE[concept_key].get("beginner")
    else:
        # Try partial matching
        for key in CONCEPT_DATABASE.keys():
            if key in concept_key or concept_key in key:
                concept_data = CONCEPT_DATABASE[key].get(difficulty)
                if not concept_data:
                    concept_data = CONCEPT_DATABASE[key].get("beginner")
                concept_key = key
                break

    # If still no match, provide a general response
    if not concept_data:
        logger.warning(f"Concept not found: {concept_key}")
        return ConceptResponse(
            concept=request.concept,
            explanation=f"I don't have detailed information about '{request.concept}' yet, but I can help you understand it! Could you provide more context or try rephrasing? For example, if you're asking about loops, try 'explain loops' or 'how do for loops work'.",
            examples=[
                "# General Python syntax\nprint('Hello, World!')",
                "# Variables and basic operations\nx = 10\ny = 20\nresult = x + y\nprint(result)"
            ],
            common_mistakes=[
                "Make sure to check spelling and try common Python terms",
                "Try asking about: loops, variables, functions, lists, conditionals"
            ],
            related_concepts=["Python basics", "data types", "control flow"],
            difficulty=difficulty
        )

    return ConceptResponse(
        concept=concept_key,
        explanation=concept_data["explanation"],
        examples=concept_data["examples"],
        common_mistakes=concept_data["common_mistakes"],
        related_concepts=concept_data["related_concepts"],
        difficulty=difficulty
    )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Concepts Agent - Python Concept Explainer",
        "endpoints": {
            "/explain": "POST - Explain a Python concept",
            "/health": "GET - Health check",
            "/concepts": "GET - List available concepts"
        }
    }

@app.get("/concepts")
async def list_concepts():
    """List all available concepts"""
    return {
        "concepts": list(CONCEPT_DATABASE.keys()),
        "count": len(CONCEPT_DATABASE)
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
