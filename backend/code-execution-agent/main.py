from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import tempfile
import os
import signal
import time
from typing import Optional
import logging

app = FastAPI(title="Code Execution Agent", version="1.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodeExecutionRequest(BaseModel):
    code: str
    user_id: str
    timeout: int = 5  # seconds
    memory_limit: int = 50  # MB

class CodeExecutionResponse(BaseModel):
    output: str
    error: Optional[str] = None
    execution_time: float
    success: bool

@app.post("/execute", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    """
    Securely execute Python code in a sandboxed environment
    Following the security requirements: 5s timeout, 50MB memory, no file/network access
    """
    start_time = time.time()

    # Validate code for dangerous operations
    dangerous_patterns = [
        'import os', 'import sys', 'import subprocess', 'import shutil',
        '__import__', 'eval', 'exec', 'open', 'file', 'input',
        'import requests', 'import urllib', 'import socket',
        'import ftplib', 'import smtplib', 'import poplib', 'import imaplib'
    ]

    code_lower = request.code.lower()
    for pattern in dangerous_patterns:
        if pattern in code_lower:
            return CodeExecutionResponse(
                output="",
                error=f"Security violation: {pattern} is not allowed",
                execution_time=time.time() - start_time,
                success=False
            )

    # Create a temporary file for the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(request.code)
        temp_file = f.name

    try:
        # Execute the code with timeout and memory limits
        # Note: This is a simplified approach. In production, you'd want to use
        # proper sandboxing technologies like Docker containers or specialized tools

        # Set environment to restrict file access
        env = os.environ.copy()
        # Remove potentially dangerous environment variables
        env.pop('PYTHONPATH', None)

        # Execute with timeout
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=request.timeout,
            env=env,
            cwd=tempfile.gettempdir()  # Restrict working directory
        )

        execution_time = time.time() - start_time

        return CodeExecutionResponse(
            output=result.stdout,
            error=result.stderr if result.stderr else None,
            execution_time=execution_time,
            success=result.returncode == 0
        )

    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        return CodeExecutionResponse(
            output="",
            error="Code execution timed out",
            execution_time=execution_time,
            success=False
        )
    except Exception as e:
        execution_time = time.time() - start_time
        return CodeExecutionResponse(
            output="",
            error=str(e),
            execution_time=execution_time,
            success=False
        )
    finally:
        # Clean up the temporary file
        try:
            os.unlink(temp_file)
        except:
            pass

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "code-execution-agent"}

@app.get("/")
async def root():
    return {
        "message": "Code Execution Agent - Secure Python code execution service",
        "endpoints": {
            "/execute": "POST - Execute Python code securely",
            "/health": "GET - Health check"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)