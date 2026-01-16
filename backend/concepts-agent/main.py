from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
from typing import Dict, Any, List
import asyncio

# Initialize FastAPI app
app = FastAPI(title="Concepts Agent", description="Explains Python concepts with examples", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConceptRequest(BaseModel):
    concept: str
    difficulty_level: str = "intermediate"  # beginner, intermediate, advanced
    user_context: Dict[str, Any] = {}
    examples_requested: bool = True

class ConceptResponse(BaseModel):
    concept: str
    explanation: str
    examples: List[str]
    related_concepts: List[str]
    difficulty_level: str
    code_samples: List[str]

# Knowledge base of Python concepts
CONCEPT_KNOWLEDGE_BASE = {
    "variables": {
        "beginner": {
            "explanation": "Variables are names that store values in Python. Think of them as labeled boxes where you can store information.",
            "examples": [
                "Creating a variable: name = 'Alice'",
                "Assigning a number: age = 25",
                "Updating a variable: age = age + 1"
            ],
            "code_samples": [
                "# Variable assignment\nname = 'Alice'\nage = 25\nprint(f'Hello {name}, you are {age} years old')"
            ]
        },
        "intermediate": {
            "explanation": "Variables in Python are references to objects in memory. They follow dynamic typing and can hold any type of value.",
            "examples": [
                "Dynamic typing: a variable can change types",
                "Variable scope: local vs global",
                "Variable naming conventions: snake_case"
            ],
            "code_samples": [
                "# Dynamic typing\nx = 10  # integer\nx = 'hello'  # string\nx = [1, 2, 3]  # list\n\n# Variable scope\nname = 'global'\ndef func():\n    name = 'local'\n    return name"
            ]
        },
        "advanced": {
            "explanation": "Python variables are references to objects. Understanding mutability, object identity, and scope resolution is crucial.",
            "examples": [
                "Mutable vs immutable objects",
                "Variable binding and closures",
                "Global and nonlocal keywords"
            ],
            "code_samples": [
                "# Mutability\noriginal_list = [1, 2, 3]\ncopied_list = original_list  # Both reference same object\ncopied_list.append(4)\nprint(original_list)  # [1, 2, 3, 4] - original changed!\n\n# Identity check\nlist1 = [1, 2, 3]\nlist2 = [1, 2, 3]\nprint(list1 is list2)  # False - different objects\nprint(list1 == list2)  # True - same content"
            ]
        }
    },
    "loops": {
        "beginner": {
            "explanation": "Loops allow you to repeat code multiple times. Python has two types: for loops and while loops.",
            "examples": [
                "For loop: iterate over a sequence",
                "While loop: repeat while condition is true",
                "Range function: generate sequences of numbers"
            ],
            "code_samples": [
                "# For loop\nfruits = ['apple', 'banana', 'cherry']\nfor fruit in fruits:\n    print(fruit)\n\n# While loop\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1"
            ]
        },
        "intermediate": {
            "explanation": "Loop controls like break, continue, and else clause provide fine-grained control over loop execution.",
            "examples": [
                "Break: exit loop early",
                "Continue: skip current iteration",
                "Else: execute when loop completes normally"
            ],
            "code_samples": [
                "# Break and continue\nnumbers = [1, 2, 3, 4, 5]\nfor num in numbers:\n    if num == 3:\n        continue  # Skip 3\n    if num == 5:\n        break  # Stop at 5\n    print(num)\n\n# Else clause\nfor i in range(3):\n    print(i)\nelse:\n    print('Loop completed normally')"
            ]
        },
        "advanced": {
            "explanation": "Advanced looping includes list comprehensions, generator expressions, and iterator protocols.",
            "examples": [
                "List comprehensions: concise loop expressions",
                "Generator expressions: memory-efficient iteration",
                "Iterator protocol: __iter__ and __next__ methods"
            ],
            "code_samples": [
                "# List comprehension\nnumbers = [1, 2, 3, 4, 5]\nsquares = [x**2 for x in numbers if x % 2 == 0]\n\n# Generator expression\nsum_of_squares = sum(x**2 for x in numbers if x % 2 == 0)\n\n# Nested comprehensions\nmatrix = [[j for j in range(3)] for i in range(3)]"
            ]
        }
    },
    "functions": {
        "beginner": {
            "explanation": "Functions are reusable blocks of code that perform a specific task. They help organize code and avoid repetition.",
            "examples": [
                "Define a function with def",
                "Call a function by name",
                "Return values from functions"
            ],
            "code_samples": [
                "# Function definition\ndef greet(name):\n    return f'Hello, {name}!'\n\n# Function call\nmessage = greet('Alice')\nprint(message)  # Hello, Alice!"
            ]
        },
        "intermediate": {
            "explanation": "Functions can have parameters, return values, and default arguments. Understanding scope is important.",
            "examples": [
                "Default parameters: provide fallback values",
                "Keyword arguments: call with named parameters",
                "Scope: local vs global variables in functions"
            ],
            "code_samples": [
                "# Default parameters\ndef introduce(name, age=18, city='Unknown'):\n    return f'{name} is {age} years old and lives in {city}'\n\n# Keyword arguments\nresult = introduce(age=25, name='Bob')\n\n# Scope\nglobal_var = 'accessible everywhere'\ndef my_func():\n    local_var = 'only in function'\n    return global_var + ' ' + local_var"
            ]
        },
        "advanced": {
            "explanation": "Advanced function concepts include decorators, closures, and first-class functions.",
            "examples": [
                "Decorators: modify function behavior",
                "Closures: functions that remember outer scope",
                "Higher-order functions: functions that take other functions"
            ],
            "code_samples": [
                "# Decorator example\ndef timer(func):\n    import time\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        end = time.time()\n        print(f'{func.__name__} took {end-start:.2f}s')\n        return result\n    return wrapper\n\n@timer\ndef slow_function():\n    import time\n    time.sleep(1)\n    return 'Done'\n\n# Closure example\ndef make_multiplier(n):\n    def multiplier(x):\n        return x * n\n    return multiplier\ndouble = make_multiplier(2)"
            ]
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
    Explain a Python concept with examples tailored to difficulty level
    """
    concept = request.concept.lower().strip()
    difficulty = request.difficulty_level

    # Validate difficulty level
    if difficulty not in ["beginner", "intermediate", "advanced"]:
        difficulty = "intermediate"

    # Check if concept exists in knowledge base
    if concept in CONCEPT_KNOWLEDGE_BASE:
        concept_data = CONCEPT_KNOWLEDGE_BASE[concept]

        if difficulty in concept_data:
            data = concept_data[difficulty]
            return ConceptResponse(
                concept=concept,
                explanation=data["explanation"],
                examples=data["examples"],
                related_concepts=[k for k in CONCEPT_KNOWLEDGE_BASE.keys() if k != concept][:3],
                difficulty_level=difficulty,
                code_samples=data["code_samples"]
            )
        else:
            # If specific difficulty not available, try intermediate then beginner
            for fallback_difficulty in ["intermediate", "beginner"]:
                if fallback_difficulty in concept_data:
                    data = concept_data[fallback_difficulty]
                    logger.warning(f"Difficulty {difficulty} not available for {concept}, falling back to {fallback_difficulty}")
                    return ConceptResponse(
                        concept=concept,
                        explanation=data["explanation"],
                        examples=data["examples"],
                        related_concepts=[k for k in CONCEPT_KNOWLEDGE_BASE.keys() if k != concept][:3],
                        difficulty_level=fallback_difficulty,
                        code_samples=data["code_samples"]
                    )

    # If concept not found, provide a generic response
    logger.warning(f"Concept '{concept}' not found in knowledge base")
    return ConceptResponse(
        concept=concept,
        explanation=f"I don't have specific information about '{concept}' in my knowledge base. Python concepts generally include variables, data types, control structures, functions, classes, and modules.",
        examples=[f"Study the basics of {concept} in Python documentation"],
        related_concepts=list(CONCEPT_KNOWLEDGE_BASE.keys())[:3],
        difficulty_level=difficulty,
        code_samples=[f"# Example placeholder for {concept}\n# See Python documentation for details"]
    )

@app.get("/concepts")
async def list_concepts():
    """List all available concepts in the knowledge base"""
    return {"concepts": list(CONCEPT_KNOWLEDGE_BASE.keys())}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)