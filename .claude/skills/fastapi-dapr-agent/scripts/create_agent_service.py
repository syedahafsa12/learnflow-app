#!/usr/bin/env python3
"""
Create a new FastAPI service with Dapr integration for AI agents
"""

import os
import sys
import argparse
from pathlib import Path

def create_service_structure(service_name, service_type="generic"):
    """Create the directory structure and files for a new service."""

    # Validate service name
    if not service_name.replace('_', '').replace('-', '').isalnum():
        raise ValueError("Service name must contain only alphanumeric characters, hyphens, and underscores")

    service_dir = Path(service_name)
    service_dir.mkdir(exist_ok=True)

    # Define the service types and their characteristics
    service_templates = {
        "triage": {
            "description": "Routes queries to appropriate specialist agents",
            "imports": ["openai", "os"],
            "endpoints": ["POST /route_query"]
        },
        "concepts": {
            "description": "Explains Python concepts with examples",
            "imports": ["openai", "os"],
            "endpoints": ["POST /explain_concept", "POST /generate_example"]
        },
        "code-review": {
            "description": "Reviews student code for correctness and style",
            "imports": ["openai", "os", "ast"],
            "endpoints": ["POST /review_code", "POST /suggest_improvements"]
        },
        "debug": {
            "description": "Helps students debug their code",
            "imports": ["openai", "os", "traceback"],
            "endpoints": ["POST /analyze_error", "POST /provide_hint"]
        },
        "exercise": {
            "description": "Generates and grades coding exercises",
            "imports": ["openai", "os", "random"],
            "endpoints": ["POST /generate_exercise", "POST /grade_submission"]
        },
        "progress": {
            "description": "Tracks and reports student progress",
            "imports": ["psycopg2", "os", "json"],
            "endpoints": ["GET /progress_report", "POST /update_progress"]
        },
        "generic": {
            "description": "Generic AI agent service",
            "imports": ["openai", "os"],
            "endpoints": ["POST /process_request"]
        }
    }

    # Get the service template
    template = service_templates.get(service_type, service_templates["generic"])

    # Create main.py
    main_py_content = f'''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import asyncio
import os
from dapr.ext.fastapi import DaprApp

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="{service_name.title()} Service",
             description="{template['description']}",
             version="1.0.0")

# Initialize Dapr extension
dapr_app = DaprApp(app)

class QueryRequest(BaseModel):
    query: str
    user_id: int
    context: dict = {{}}

@app.get("/")
async def root():
    return {{"message": "Welcome to {service_name} service", "status": "healthy"}}

@app.get("/health")
async def health_check():
    return {{"status": "healthy", "service": "{service_name}"}}

'''

    # Add service-specific endpoints based on type
    if service_type == "triage":
        main_py_content += '''@app.post("/route_query")
async def route_query(request: QueryRequest):
    """
    Route queries to appropriate specialist agents
    """
    logger.info(f"Routing query: {{request.query[:50]}}...")

    # Logic to determine which agent to route to
    if "explain" in request.query.lower() or "what is" in request.query.lower():
        agent = "concepts"
    elif "error" in request.query.lower() or "not working" in request.query.lower():
        agent = "debug"
    elif "review" in request.query.lower() or "check" in request.query.lower():
        agent = "code-review"
    elif "exercise" in request.query.lower() or "quiz" in request.query.lower():
        agent = "exercise"
    else:
        agent = "concepts"  # Default

    response = {{
        "target_agent": agent,
        "original_query": request.query,
        "routing_confidence": 0.8
    }}

    return response
'''
    elif service_type == "concepts":
        main_py_content += '''@app.post("/explain_concept")
async def explain_concept(request: QueryRequest):
    """
    Explain Python concepts with examples
    """
    logger.info(f"Explaining concept: {{request.query}}")

    # In a real implementation, this would call an LLM
    response = {{
        "concept": request.query,
        "explanation": f"Explanation of {{request.query}} would go here",
        "examples": ["Example 1", "Example 2"],
        "difficulty_level": "intermediate"
    }}

    return response

@app.post("/generate_example")
async def generate_example(request: QueryRequest):
    """
    Generate code examples for concepts
    """
    logger.info(f"Generating example for: {{request.query}}")

    response = {{
        "concept": request.query,
        "example_code": "# Generated example code would go here",
        "explanation": "How the example works"
    }}

    return response
'''
    elif service_type == "code-review":
        main_py_content += '''@app.post("/review_code")
async def review_code(request: QueryRequest):
    """
    Review student code for correctness and style
    """
    logger.info(f"Reviewing code: {{request.query[:30]}}...")

    response = {{
        "code": request.query,
        "issues": [],
        "suggestions": [],
        "rating": 5,
        "feedback": "Code looks good!"
    }}

    return response

@app.post("/suggest_improvements")
async def suggest_improvements(request: QueryRequest):
    """
    Suggest improvements to student code
    """
    logger.info(f"Suggesting improvements: {{request.query[:30]}}...")

    response = {{
        "original_code": request.query,
        "improved_code": "# Improved version would go here",
        "reasoning": "Why these changes are better"
    }}

    return response
'''
    elif service_type == "debug":
        main_py_content += '''@app.post("/analyze_error")
async def analyze_error(request: QueryRequest):
    """
    Analyze error messages and provide solutions
    """
    logger.info(f"Analyzing error: {{request.query}}")

    response = {{
        "error_message": request.query,
        "likely_causes": ["Possible cause 1", "Possible cause 2"],
        "solutions": ["Solution 1", "Solution 2"],
        "confidence": 0.9
    }}

    return response

@app.post("/provide_hint")
async def provide_hint(request: QueryRequest):
    """
    Provide hints to help students solve problems
    """
    logger.info(f"Providing hint for: {{request.query[:30]}}...")

    response = {{
        "problem": request.query,
        "hint": "Consider reviewing the documentation for this concept",
        "next_steps": ["Step 1", "Step 2"]
    }}

    return response
'''
    elif service_type == "exercise":
        main_py_content += '''@app.post("/generate_exercise")
async def generate_exercise(request: QueryRequest):
    """
    Generate coding exercises
    """
    logger.info(f"Generating exercise for topic: {{request.query}}")

    response = {{
        "topic": request.query,
        "exercise_title": f"Exercise on {{request.query}}",
        "description": "Exercise description would go here",
        "starter_code": "# Starter code for exercise",
        "solution": "# Solution code would go here",
        "difficulty": "intermediate"
    }}

    return response

@app.post("/grade_submission")
async def grade_submission(request: QueryRequest):
    """
    Grade student code submissions
    """
    logger.info(f"Grading submission: {{request.query[:30]}}...")

    response = {{
        "submission": request.query,
        "passed": True,
        "score": 100,
        "feedback": "Great job!",
        "suggestions": []
    }}

    return response
'''
    elif service_type == "progress":
        main_py_content += '''@app.get("/progress_report")
async def progress_report(user_id: int):
    """
    Get progress report for a user
    """
    logger.info(f"Getting progress report for user: {{user_id}}")

    response = {{
        "user_id": user_id,
        "overall_progress": 45,
        "module_progress": [
            {{"module": "Basics", "progress": 100}},
            {{"module": "Control Flow", "progress": 75}},
            {{"module": "Data Structures", "progress": 30}}
        ],
        "recent_activity": ["Completed exercise", "Reviewed concept"],
        "recommendations": ["Review conditionals", "Practice loops"]
    }}

    return response

@app.post("/update_progress")
async def update_progress(request: QueryRequest):
    """
    Update progress for a user
    """
    logger.info(f"Updating progress for user: {{request.user_id}}")

    response = {{
        "user_id": request.user_id,
        "updated_field": "progress",
        "success": True,
        "new_value": "Updated successfully"
    }}

    return response
'''
    else:  # generic
        main_py_content += '''@app.post("/process_request")
async def process_request(request: QueryRequest):
    """
    Process a generic request
    """
    logger.info(f"Processing request: {{request.query[:50]}}...")

    response = {{
        "request_id": "req_" + str(hash(request.query))[:8],
        "processed_query": request.query,
        "result": "Processed successfully",
        "context": request.context
    }}

    return response
'''

    # Write main.py
    with open(service_dir / "main.py", "w") as f:
        f.write(main_py_content)

    # Create requirements.txt
    requirements_content = '''fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
dapr-ext-fastapi==1.8.0
python-multipart==0.0.6
requests==2.31.0
'''
    if "openai" in template['imports']:
        requirements_content += "openai==1.3.5\n"
    if "psycopg2" in template['imports']:
        requirements_content += "psycopg2-binary==2.9.7\n"

    with open(service_dir / "requirements.txt", "w") as f:
        f.write(requirements_content)

    # Create Dockerfile
    dockerfile_content = f'''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
    with open(service_dir / "Dockerfile", "w") as f:
        f.write(dockerfile_content)

    # Create dapr configuration
    dapr_config = f'''apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
---
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
'''
    with open(service_dir / f"{service_name}_dapr.yaml", "w") as f:
        f.write(dapr_config)

    # Create k8s deployment manifest
    k8s_manifest = f'''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  labels:
    app: {service_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "{service_name}"
        dapr.io/app-port: "8000"
        dapr.io/log-as-json: "true"
    spec:
      containers:
      - name: {service_name}
        image: {service_name}:latest
        ports:
        - containerPort: 8000
        env:
        - name: DAPR_HTTP_PORT
          value: "3500"
        - name: DAPR_GRPC_PORT
          value: "50001"
---
apiVersion: v1
kind: Service
metadata:
  name: {service_name}-service
spec:
  selector:
    app: {service_name}
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
'''
    with open(service_dir / f"{service_name}_deployment.yaml", "w") as f:
        f.write(k8s_manifest)

def main():
    parser = argparse.ArgumentParser(description='Create a new FastAPI service with Dapr integration')
    parser.add_argument('service_name', help='Name of the service to create')
    parser.add_argument('--type', '-t', choices=[
        'triage', 'concepts', 'code-review', 'debug', 'exercise', 'progress', 'generic'
    ], default='generic', help='Type of AI agent service to create')

    args = parser.parse_args()

    try:
        print(f"Creating {args.type} service: {args.service_name}")
        create_service_structure(args.service_name, args.type)
        print(f"✓ Service '{args.service_name}' created successfully!")
        print(f"  - Directory: {args.service_name}/")
        print(f"  - Main file: {args.service_name}/main.py")
        print(f"  - Requirements: {args.service_name}/requirements.txt")
        print(f"  - Dockerfile: {args.service_name}/Dockerfile")
        print(f"  - Dapr config: {args.service_name}/{args.service_name}_dapr.yaml")
        print(f"  - K8s manifest: {args.service_name}/{args.service_name}_deployment.yaml")

    except Exception as e:
        print(f"✗ Error creating service: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()