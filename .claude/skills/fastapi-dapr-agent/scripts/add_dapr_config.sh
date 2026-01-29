#!/bin/bash

# Dapr Configuration Script
# Adds Dapr configuration to a FastAPI service

set -e  # Exit on any error

if [ $# -eq 0 ]; then
    echo "Usage: $0 <service_name>"
    exit 1
fi

SERVICE_NAME=$1
SERVICE_DIR="./${SERVICE_NAME}"

echo "Adding Dapr configuration to service: $SERVICE_NAME"

# Create Dapr component configurations
mkdir -p "$SERVICE_DIR/dapr-components"

# Create state store component (Redis by default)
cat > "$SERVICE_DIR/dapr-components/statestore.yaml" << COMPONENT_EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master:6379
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"
COMPONENT_EOF

# Create pub/sub component (Redis by default)
cat > "$SERVICE_DIR/dapr-components/pubsub.yaml" << PUBSUB_EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master:6379
  - name: redisPassword
    value: ""
PUBSUB_EOF

# Create configuration file
cat > "$SERVICE_DIR/dapr-components/config.yaml" << CONFIG_EOF
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: dapr-config
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
CONFIG_EOF

# Update main.py to use Dapr properly
cat > "$SERVICE_DIR/main.py" << PYTHON_EOF
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncio
import logging
import os
import json
from typing import Dict, Optional

# Import Dapr client
try:
    from dapr.aio.clients import DaprClient
    import dapr.ext.grpc as grpc_ext
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

# Global Dapr client for reuse
dapr_client = None

@app.on_event('startup')
async def startup_event():
    global dapr_client
    if DaprClient:
        dapr_client = DaprClient()

@app.on_event('shutdown')
async def shutdown_event():
    global dapr_client
    if dapr_client:
        await dapr_client.close()

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
        if dapr_client:
            # Save the interaction to state
            await dapr_client.save_state(
                store_name="statestore",
                key=f"interaction-{request.user_id}-{abs(hash(request.query))}",
                value={
                    "query": request.query, 
                    "response": response_text, 
                    "timestamp": asyncio.get_event_loop().time(),
                    "user_id": request.user_id
                }
            )
            
            # Publish an event to the pub/sub system
            await dapr_client.publish_event(
                pubsub_name="pubsub",
                topic_name="ai.interactions",
                data=json.dumps({
                    "service": "$SERVICE_NAME",
                    "user_id": request.user_id,
                    "query": request.query,
                    "response": response_text
                }),
                data_content_type="application/json"
            )
        
        return QueryResponse(
            result=response_text,
            metadata={"service": "$SERVICE_NAME", "processed_by": "AI Agent", "user_id": request.user_id}
        )
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/state/{key}")
async def get_state(key: str):
    """
    Retrieve state from Dapr state store
    """
    if dapr_client:
        state = await dapr_client.get_state(store_name="statestore", key=key)
        return {"key": key, "value": state.data.decode() if state.data else None}
    else:
        return {"key": key, "value": "Dapr not available"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
PYTHON_EOF

echo "✓ Dapr configuration added to service '$SERVICE_NAME'!"
echo "Components created: statestore, pubsub"
echo "Configuration: tracing enabled"
echo "Updated main.py with proper Dapr integration"
