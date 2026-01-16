from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
from typing import Dict, Any, List
import re
import traceback

# Initialize FastAPI app
app = FastAPI(title="Debug Agent", description="Helps students debug errors and provides hints", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DebugRequest(BaseModel):
    error_message: str
    code: str = ""
    language: str = "python"
    user_context: Dict[str, Any] = {}

class DebugSuggestion(BaseModel):
    type: str  # error, hint, fix
    severity: str  # low, medium, high, critical
    description: str
    solution: str
    example: str

class DebugResponse(BaseModel):
    error_type: str
    description: str
    suggestions: List[DebugSuggestion]
    confidence: float
    quick_fix: str

# Common Python error patterns and solutions
ERROR_PATTERNS = {
    # Syntax errors
    r"(SyntaxError).*: invalid syntax": {
        "type": "syntax",
        "description": "There's an issue with the syntax of your code",
        "suggestions": [{
            "type": "error",
            "severity": "high",
            "description": "Invalid syntax detected",
            "solution": "Check for missing colons, parentheses, brackets, or quotes",
            "example": "if x == 5:  # Colon was missing\n    print('x is 5')"
        }]
    },
    r"(IndentationError).*": {
        "type": "indentation",
        "description": "Incorrect indentation in your code",
        "suggestions": [{
            "type": "error",
            "severity": "high",
            "description": "Improper indentation",
            "solution": "Make sure to use consistent indentation (spaces or tabs, but not mixed)",
            "example": "# Correct indentation\nif x > 0:\n    print('Positive')\n    if x > 10:\n        print('Greater than 10')"
        }]
    },
    r"(NameError).*name '(\w+)' is not defined": {
        "type": "name",
        "description": "A variable or function name is not recognized",
        "suggestions": [{
            "type": "error",
            "severity": "high",
            "description": "Variable or function not defined",
            "solution": "Check that the variable or function is defined before you use it",
            "example": "# Define before using\nmy_variable = 'Hello'\nprint(my_variable)  # Was causing NameError"
        }]
    },
    r"(TypeError).*unsupported operand type": {
        "type": "type",
        "description": "Trying to perform an operation on incompatible types",
        "suggestions": [{
            "type": "error",
            "severity": "high",
            "description": "Type mismatch in operation",
            "solution": "Convert types appropriately before the operation",
            "example": "# Convert string to int before arithmetic\nage = '25'\nnext_year = int(age) + 1  # Convert string to int"
        }]
    },
    r"(AttributeError).*object has no attribute '(\w+)'": {
        "type": "attribute",
        "description": "Trying to access an attribute or method that doesn't exist",
        "suggestions": [{
            "type": "error",
            "severity": "high",
            "description": "Attribute does not exist",
            "solution": "Check the spelling of the attribute/method or verify the object type",
            "example": "# Correct attribute name\nmy_list = [1, 2, 3]\nlength = my_list.len()  # Wrong - should be len(my_list) or my_list.__len__()"
        }]
    },
    r"(ValueError).*": {
        "type": "value",
        "description": "A function received an argument of the right type but inappropriate value",
        "suggestions": [{
            "type": "error",
            "severity": "medium",
            "description": "Invalid value for operation",
            "solution": "Check the values being passed to functions",
            "example": "# Valid value for conversion\nnumber_str = '123abc'\n# This causes ValueError, need to ensure it's a valid number\ntry:\n    number = int(number_str)\nexcept ValueError:\n    print('Invalid number format')"
        }]
    },
    r"(IndexError).*": {
        "type": "index",
        "description": "Trying to access an index that doesn't exist",
        "suggestions": [{
            "type": "error",
            "severity": "high",
            "description": "Index out of range",
            "solution": "Check array/list bounds before accessing elements",
            "example": "# Safe indexing\nmy_list = [1, 2, 3]\nindex = 5\nif 0 <= index < len(my_list):\n    value = my_list[index]\nelse:\n    print('Index out of range')"
        }]
    },
    r"(KeyError).*": {
        "type": "key",
        "description": "Trying to access a dictionary key that doesn't exist",
        "suggestions": [{
            "type": "error",
            "severity": "high",
            "description": "Dictionary key not found",
            "solution": "Check if key exists before accessing or use .get() method",
            "example": "# Safe key access\nmy_dict = {'a': 1, 'b': 2}\nkey = 'c'\nif key in my_dict:\n    value = my_dict[key]\n# Or use get method\nvalue = my_dict.get(key, 'default_value')"
        }]
    },
    r"(ImportError).*": {
        "type": "import",
        "description": "Unable to import a module",
        "suggestions": [{
            "type": "error",
            "severity": "high",
            "description": "Module import failed",
            "solution": "Check if the module is installed and the name is spelled correctly",
            "example": "# Install missing package\n# pip install requests\nimport requests  # Module must be installed"
        }]
    }
}

def analyze_error_message(error_msg: str) -> Dict[str, Any]:
    """Analyze error message and provide appropriate suggestions"""
    for pattern, info in ERROR_PATTERNS.items():
        if re.search(pattern, error_msg, re.IGNORECASE):
            return {
                "type": info["type"],
                "description": info["description"],
                "suggestions": info["suggestions"]
            }

    # If no specific pattern matched, provide general debugging advice
    return {
        "type": "general",
        "description": "An error occurred in your code",
        "suggestions": [{
            "type": "hint",
            "severity": "medium",
            "description": "General debugging tip",
            "solution": "Read the error message carefully. It usually tells you what went wrong and where.",
            "example": "# Example error message breakdown\n# Traceback (most recent call last):\n# File \"main.py\", line 5, in <module>\n# NameError: name 'x' is not defined\n# This means: In file main.py, line 5, there's a NameError because 'x' is not defined"
        }]
    }

def extract_code_context(error_msg: str, code: str) -> str:
    """Extract relevant code context based on error message"""
    # Try to find line number from error message
    line_match = re.search(r"line (\d+)", error_msg)
    if line_match:
        try:
            line_num = int(line_match.group(1))
            lines = code.split('\n')
            if 0 < line_num <= len(lines):
                # Return the problematic line plus context
                start = max(0, line_num - 3)
                end = min(len(lines), line_num + 2)
                context = []
                for i in range(start, end):
                    marker = ">>> " if i == line_num - 1 else "    "
                    context.append(f"{marker}{i+1:3d}: {lines[i]}")
                return "\n".join(context)
        except:
            pass

    return ""

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "debug-agent"}

@app.post("/debug", response_model=DebugResponse)
async def debug_error(request: DebugRequest):
    """
    Analyze error message and provide debugging suggestions
    """
    logger.info(f"Debugging error: {request.error_message[:100]}...")

    # Analyze the error message
    analysis = analyze_error_message(request.error_message)

    # Extract code context if code was provided
    code_context = extract_code_context(request.error_message, request.code)

    # Calculate confidence based on how specific the error is
    confidence = 0.8 if analysis["type"] != "general" else 0.5

    # Prepare quick fix if possible
    quick_fix = "Review the suggestions below to fix the error"
    if analysis["suggestions"]:
        # Create a simple quick fix based on the first suggestion
        first_suggestion = analysis["suggestions"][0]
        if "convert" in first_suggestion["solution"].lower():
            quick_fix = "Try converting types appropriately"
        elif "colon" in first_suggestion["solution"].lower():
            quick_fix = "Check for missing colons after statements"
        elif "indentation" in first_suggestion["solution"].lower():
            quick_fix = "Fix the indentation in your code"
        elif "defined" in first_suggestion["solution"].lower():
            quick_fix = "Make sure all variables are defined before use"

    logger.info(f"Debug analysis completed for error type: {analysis['type']}")

    return DebugResponse(
        error_type=analysis["type"],
        description=analysis["description"],
        suggestions=analysis["suggestions"],
        confidence=confidence,
        quick_fix=quick_fix
    )

@app.post("/analyze-full")
async def analyze_full_debug(request: DebugRequest):
    """
    Provide a more comprehensive debug analysis
    """
    # Perform the basic debug
    basic_response = await debug_error(request)

    # Add additional analysis if code is provided
    if request.code.strip():
        additional_suggestions = []

        # Check for common Python mistakes in the code
        lines = request.code.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for missing colon after control statements
            if re.match(r'^\s*(if|for|while|def|class|try|except|with)\s+', line) and not line.rstrip().endswith(':'):
                additional_suggestions.append({
                    "type": "hint",
                    "severity": "high",
                    "description": f"Missing colon on line {i}",
                    "solution": "Add a colon at the end of this line",
                    "example": f"{line}  # Add ':' at the end -> {line}:"
                })

            # Check for assignment instead of equality in condition
            if 'if ' in line and re.search(r'if .*= [^=]', line):
                additional_suggestions.append({
                    "type": "hint",
                    "severity": "high",
                    "description": f"Possible assignment instead of equality check on line {i}",
                    "solution": "Use == for comparison in conditions",
                    "example": f"{line}  # Use '==' instead of '='"
                })

        # Add additional suggestions to the response
        if additional_suggestions:
            # Convert dict to DebugSuggestion objects
            new_suggestions = [DebugSuggestion(**s) for s in additional_suggestions]
            basic_response.suggestions.extend(new_suggestions)

    return basic_response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)