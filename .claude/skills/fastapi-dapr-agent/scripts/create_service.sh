#!/bin/bash

# FastAPI Dapr Service Creation Script
# Creates a new FastAPI service with Dapr integration

set -e  # Exit on any error

if [ $# -eq 0 ]; then
    echo "Usage: $0 <service_name>"
    exit 1
fi

SERVICE_NAME=$1
SERVICE_DIR="./${SERVICE_NAME}"

echo "Creating FastAPI Dapr service: $SERVICE_NAME"

# Create service directory
mkdir -p "$SERVICE_DIR"

# Create main.py with FastAPI and Dapr integration
cat > "$SERVICE_DIR/main.py" << PYTHON_EOF
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import logging
import os

# Import Dapr client
try:
    from dapr.aio.clients import DaprClient
    from dapr.ext.grpc import App
except ImportError:
    print("Dapr libraries not available in dev environment, using mock for now")
    DaprClient = None

app = FastAPI(title="$SERVICE_NAME Service", description="AI agent service with Dapr integration")

# Example request/response models
class QueryRequest(BaseModel):
    user_id: str
    query: str
    context: dict = {}

class QueryResponse(BaseModel):
    result: str
    metadata: dict = {}

@app.get("/")
async def root():
    return {"message": "$SERVICE_NAME service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a query from the user and return a response.
    This is where the AI agent logic would be implemented.
    """
    try:
        # Log the incoming request
        print(f"Processing query for user {request.user_id}: {request.query}")
        
        # Simulate AI processing (replace with actual AI logic)
        response_text = f"This is a simulated response from $SERVICE_NAME for query: '{request.query}'"
        
        # Example of how to use Dapr for state management
        if DaprClient:
            async with DaprClient() as client:
                # Save the interaction to state
                await client.save_state(
                    store_name="statestore",
                    key=f"interaction-{request.user_id}-{hash(request.query)}",
                    value={"query": request.query, "response": response_text, "timestamp": str(asyncio.get_event_loop().time())}
                )
        
        return QueryResponse(
            result=response_text,
            metadata={"service": "$SERVICE_NAME", "processed_by": "AI Agent"}
        )
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
PYTHON_EOF

# Create requirements.txt
cat > "$SERVICE_DIR/requirements.txt" << REQUIREMENTS_EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
dapr==1.12.0
grpcio==1.60.0
asyncio==3.4.3
requests==2.31.0
REQUIREMENTS_EOF

# Create Dockerfile
cat > "$SERVICE_DIR/Dockerfile" << DOCKERFILE_EOF
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
DOCKERFILE_EOF

echo "✓ FastAPI Dapr service '$SERVICE_NAME' created successfully!"
echo "Service directory: $SERVICE_DIR"
echo "Files created: main.py, requirements.txt, Dockerfile"
