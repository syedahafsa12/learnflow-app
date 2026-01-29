from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from typing import Dict, Any, List
import re

app = FastAPI(title="Code Review Agent", version="1.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodeReviewRequest(BaseModel):
    code: str
    feedback_type: str = "comprehensive"  # comprehensive, style, efficiency
    user_context: Dict[str, Any] = {}

class CodeReviewIssue(BaseModel):
    line: int
    severity: str  # error, warning, suggestion
    category: str  # style, efficiency, correctness, security
    message: str
    suggestion: str

class CodeReviewResponse(BaseModel):
    issues: List[CodeReviewIssue]
    summary: str
    score: float  # 0-100
    recommendations: List[str]

@app.post("/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    """Review Python code for quality, style, and best practices"""
    logger.info(f"Reviewing code for user: {request.user_context.get('user_id', 'unknown')}")

    issues = []
    recommendations = []

    # Check for common Python style issues (PEP 8)
    lines = request.code.split('\n')

    for i, line in enumerate(lines, 1):
        # Check line length (should be < 79 chars for PEP 8)
        if len(line) > 79:
            issues.append(CodeReviewIssue(
                line=i,
                severity="warning",
                category="style",
                message=f"Line too long ({len(line)} > 79 characters)",
                suggestion="Break line into multiple lines or reduce complexity"
            ))

        # Check for improper spacing around operators
        if '=' in line and not re.search(r'\s=\s', line) and '==' not in line and '!=' not in line:
            if re.search(r'[a-zA-Z_]\s*=', line) or re.search(r'=\s*[a-zA-Z_]', line):
                issues.append(CodeReviewIssue(
                    line=i,
                    severity="warning",
                    category="style",
                    message="Missing proper spacing around assignment operator",
                    suggestion="Add spaces around '=' operator: var = value"
                ))

    # Check for function documentation
    func_pattern = r'def\s+(\w+)\s*\([^)]*\)\s*:'
    functions = re.findall(func_pattern, request.code)

    for func_name in functions:
        # Check if the function has a docstring
        func_def_start = request.code.find(f'def {func_name}')
        if func_def_start != -1:
            # Find the line number
            lines_before = request.code[:func_def_start].count('\n')
            func_line_num = lines_before + 1

            # Check if there's a docstring after the function definition
            func_block = request.code[func_def_start:]
            end_of_def = func_block.find(':') + 1
            next_part = func_block[end_of_def:].strip()

            if not (next_part.startswith('"""') or next_part.startswith("'''")):
                issues.append(CodeReviewIssue(
                    line=func_line_num,
                    severity="suggestion",
                    category="documentation",
                    message=f"Function '{func_name}' missing docstring",
                    suggestion="Add docstring to describe function purpose, parameters, and return value"
                ))

    # Check for unused imports
    import_pattern = r'^\s*(?:import|from)\s+(\w+)'
    imports = re.findall(import_pattern, request.code, re.MULTILINE)

    for imp in imports:
        # Check if import is used in the code
        if not re.search(r'\b' + imp + r'\b', request.code.replace(f'import {imp}', '').replace(f'from {imp}', '')):
            issues.append(CodeReviewIssue(
                line=1,  # Simplified - would need better line detection
                severity="warning",
                category="efficiency",
                message=f"Unused import: {imp}",
                suggestion="Remove unused import to clean up code"
            ))

    # Generate summary and score
    error_count = len([issue for issue in issues if issue.severity == "error"])
    warning_count = len([issue for issue in issues if issue.severity == "warning"])
    suggestion_count = len([issue for issue in issues if issue.severity == "suggestion"])

    score = max(0, min(100, 100 - (error_count * 10 + warning_count * 3 + suggestion_count * 1)))

    summary = f"Found {error_count} errors, {warning_count} warnings, and {suggestion_count} suggestions. Overall quality score: {score}/100"

    recommendations = [
        "Consider adding type hints for better code clarity",
        "Use meaningful variable names",
        "Break down complex functions into smaller ones",
        "Add unit tests for your functions"
    ]

    return CodeReviewResponse(
        issues=issues,
        summary=summary,
        score=score,
        recommendations=recommendations
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "code-review-agent"}

@app.get("/")
async def root():
    return {
        "message": "Code Review Agent - Analyzes Python code quality",
        "endpoints": {
            "/review": "POST - Review Python code",
            "/health": "GET - Health check"
        }
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8004))
    uvicorn.run(app, host="0.0.0.0", port=port)
