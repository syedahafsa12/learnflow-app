from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
from typing import Dict, Any, List
import ast
import re

# Initialize FastAPI app
app = FastAPI(title="Code Review Agent", description="Analyzes code quality, style, and best practices", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"
    check_style: bool = True
    check_logic: bool = True
    check_security: bool = True
    user_context: Dict[str, Any] = {}

class Issue(BaseModel):
    type: str  # style, logic, security, performance
    severity: str  # low, medium, high, critical
    line: int
    description: str
    suggestion: str

class CodeReviewResponse(BaseModel):
    issues: List[Issue]
    score: float  # 0.0 to 1.0
    summary: str
    suggestions: List[str]

# Style guidelines for Python
PYTHON_STYLE_GUIDELINES = {
    "line_length": 88,
    "naming_patterns": {
        "variables_functions": r"^[a-z][a-z0-9_]*$",  # snake_case
        "classes": r"^[A-Z][a-zA-Z0-9]*$",  # PascalCase
        "constants": r"^[A-Z][A-Z0-9_]*$"  # UPPER_CASE
    },
    "imports_order": ["standard_library", "third_party", "local"],
    "unnecessary_semicolons": True,
    "trailing_whitespace": False
}

def analyze_code_syntax(code: str) -> List[Issue]:
    """Analyze code for syntax issues"""
    issues = []

    try:
        # Parse the code to check for syntax errors
        tree = ast.parse(code)
    except SyntaxError as e:
        issues.append(Issue(
            type="syntax",
            severity="critical",
            line=e.lineno or 0,
            description=f"Syntax error: {e.msg}",
            suggestion="Fix the syntax error in the code"
        ))
    except Exception as e:
        issues.append(Issue(
            type="parsing",
            severity="critical",
            line=0,
            description=f"Parsing error: {str(e)}",
            suggestion="Check the code structure"
        ))

    return issues

def analyze_code_style(code: str) -> List[Issue]:
    """Analyze code for style issues following PEP 8"""
    issues = []

    lines = code.split('\n')

    for i, line in enumerate(lines, 1):
        # Check line length
        if len(line) > PYTHON_STYLE_GUIDELINES["line_length"]:
            issues.append(Issue(
                type="style",
                severity="medium",
                line=i,
                description=f"Line too long ({len(line)} > {PYTHON_STYLE_GUIDELINES['line_length']} characters)",
                suggestion="Break the line into multiple lines or reduce its length"
            ))

        # Check for trailing whitespace
        if line.endswith(' ') or line.endswith('\t'):
            issues.append(Issue(
                type="style",
                severity="low",
                line=i,
                description="Trailing whitespace",
                suggestion="Remove trailing whitespace"
            ))

        # Check for unnecessary semicolons
        if line.rstrip().endswith(';'):
            issues.append(Issue(
                type="style",
                severity="low",
                line=i,
                description="Unnecessary semicolon",
                suggestion="Remove the semicolon (not needed in Python)"
            ))

    # Check naming conventions by parsing the AST
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):  # Variable assignment
                name = node.id
                if not re.match(PYTHON_STYLE_GUIDELINES["naming_patterns"]["variables_functions"], name):
                    if not (name.startswith('_') and re.match(PYTHON_STYLE_GUIDELINES["naming_patterns"]["variables_functions"], name[1:])):
                        issues.append(Issue(
                            type="style",
                            severity="medium",
                            line=node.lineno,
                            description=f"Variable name '{name}' doesn't follow snake_case convention",
                            suggestion="Use snake_case for variable names (e.g., my_variable)"
                        ))
            elif isinstance(node, ast.FunctionDef):  # Function definition
                name = node.name
                if not re.match(PYTHON_STYLE_GUIDELINES["naming_patterns"]["variables_functions"], name):
                    issues.append(Issue(
                        type="style",
                        severity="medium",
                        line=node.lineno,
                        description=f"Function name '{name}' doesn't follow snake_case convention",
                        suggestion="Use snake_case for function names (e.g., my_function)"
                    ))
            elif isinstance(node, ast.ClassDef):  # Class definition
                name = node.name
                if not re.match(PYTHON_STYLE_GUIDELINES["naming_patterns"]["classes"], name):
                    issues.append(Issue(
                        type="style",
                        severity="medium",
                        line=node.lineno,
                        description=f"Class name '{name}' doesn't follow PascalCase convention",
                        suggestion="Use PascalCase for class names (e.g., MyClass)"
                    ))
            elif isinstance(node, ast.Assign):  # Constant assignment (simple case)
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if name.isupper() and not re.match(PYTHON_STYLE_GUIDELINES["naming_patterns"]["constants"], name):
                            issues.append(Issue(
                                type="style",
                                severity="medium",
                                line=target.lineno,
                                description=f"Constant name '{name}' doesn't follow UPPER_CASE convention",
                                suggestion="Use UPPER_CASE for constants (e.g., MY_CONSTANT)"
                            ))
    except:
        # If parsing fails, skip style analysis
        pass

    return issues

def analyze_code_logic(code: str) -> List[Issue]:
    """Analyze code for logical issues"""
    issues = []

    # Parse the code
    try:
        tree = ast.parse(code)
    except:
        return issues  # Skip if syntax is invalid

    lines = code.split('\n')

    # Check for undefined variables
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            # This is a simple check - in a real system, we'd need to do proper scoping analysis
            pass

        # Check for potential infinite loops
        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Constant) and node.test.value is True:
                issues.append(Issue(
                    type="logic",
                    severity="high",
                    line=node.lineno,
                    description="Potential infinite while loop detected",
                    suggestion="Add a break condition or make the loop condition variable"
                ))

        # Check for unused variables (basic check)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    # Simple check: if it's assigned but the next line is pass or end of function, might be unused
                    pass

        # Check for unreachable code after return statements
        if isinstance(node, ast.Return):
            # Check if there are statements after return in the same block
            parent = getattr(node, 'parent', None)
            if hasattr(parent, 'body'):
                stmt_idx = -1
                for idx, stmt in enumerate(parent.body):
                    if stmt == node:
                        stmt_idx = idx
                        break

                if stmt_idx != -1 and stmt_idx < len(parent.body) - 1:
                    next_stmt = parent.body[stmt_idx + 1]
                    issues.append(Issue(
                        type="logic",
                        severity="high",
                        line=next_stmt.lineno,
                        description="Unreachable code after return statement",
                        suggestion="Remove or restructure the code after the return statement"
                    ))

    # Check for common logical errors in code strings
    for i, line in enumerate(lines, 1):
        # Check for assignment instead of equality in condition
        if 'if ' in line and '=' in line and '==' not in line and '= ' in line:
            if re.search(r'if .*=[^=].*', line):
                issues.append(Issue(
                    type="logic",
                    severity="high",
                    line=i,
                    description="Possible assignment (=) instead of equality (==) in condition",
                    suggestion="Use == for comparison in conditions"
                ))

    return issues

def analyze_code_security(code: str) -> List[Issue]:
    """Analyze code for security issues"""
    issues = []

    lines = code.split('\n')

    for i, line in enumerate(lines, 1):
        # Check for eval usage
        if 'eval(' in line:
            issues.append(Issue(
                type="security",
                severity="critical",
                line=i,
                description="Dangerous use of eval() function",
                suggestion="Avoid eval() as it can execute arbitrary code. Use ast.literal_eval() for safe evaluation of literals."
            ))

        # Check for exec usage
        if 'exec(' in line:
            issues.append(Issue(
                type="security",
                severity="critical",
                line=i,
                description="Dangerous use of exec() function",
                suggestion="Avoid exec() as it can execute arbitrary code."
            ))

        # Check for potential command injection
        if ('os.system(' in line or 'subprocess.' in line) and ('+' in line or '%' in line or '.format(' in line):
            issues.append(Issue(
                type="security",
                severity="high",
                line=i,
                description="Potential command injection vulnerability",
                suggestion="Sanitize inputs before using them in system commands. Consider using parameterized commands."
            ))

        # Check for hardcoded passwords/secrets
        if ('password' in line.lower() or 'secret' in line.lower() or 'key' in line.lower()) and '=' in line:
            if any(secret_word in line.lower() for secret_word in ['password', 'secret', 'token', 'key']):
                issues.append(Issue(
                    type="security",
                    severity="high",
                    line=i,
                    description="Hardcoded credential detected",
                    suggestion="Store credentials securely using environment variables or a secrets manager."
                ))

    return issues

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "code-review-agent"}

@app.post("/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    """
    Review code for style, logic, security, and performance issues
    """
    logger.info(f"Reviewing code of length {len(request.code)} characters")

    all_issues = []

    # Perform syntax analysis
    syntax_issues = analyze_code_syntax(request.code)
    all_issues.extend(syntax_issues)

    # Perform style analysis if requested
    if request.check_style:
        style_issues = analyze_code_style(request.code)
        all_issues.extend(style_issues)

    # Perform logic analysis if requested
    if request.check_logic:
        logic_issues = analyze_code_logic(request.code)
        all_issues.extend(logic_issues)

    # Perform security analysis if requested
    if request.check_security:
        security_issues = analyze_code_security(request.code)
        all_issues.extend(security_issues)

    # Calculate score based on issues
    max_issues_for_low_score = 5
    issue_count = len(all_issues)

    if issue_count == 0:
        score = 1.0
    elif issue_count >= max_issues_for_low_score:
        score = 0.1
    else:
        score = 1.0 - (issue_count / max_issues_for_low_score) * 0.9

    # Create summary
    if issue_count == 0:
        summary = "Code looks great! No issues detected."
    elif issue_count <= 2:
        summary = f"Code is mostly clean with {issue_count} minor issue(s)."
    elif issue_count <= 5:
        summary = f"Code has {issue_count} issues that should be addressed."
    else:
        summary = f"Code has {issue_count} issues that need attention."

    # Extract unique suggestions
    suggestions = list(set(issue.suggestion for issue in all_issues))

    logger.info(f"Code review completed with {issue_count} issues found, score: {score:.2f}")

    return CodeReviewResponse(
        issues=all_issues,
        score=score,
        summary=summary,
        suggestions=suggestions
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)