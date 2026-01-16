---
name: fastapi-dapr-agent
description: Create FastAPI services with Dapr integration for microservices architecture
---

# FastAPI Dapr Agent Setup

## When to Use
- Creating microservices with FastAPI and Dapr
- Building event-driven architectures
- Need for state management and service invocation
- Building AI agent services for LearnFlow platform

## Instructions
1. Scaffold service: `./scripts/create_fastapi_dapr_service.py <service_name>`
2. Deploy to Kubernetes: `./scripts/deploy_fastapi_dapr.sh <service_name>`
3. Verify deployment: `python scripts/verify_fastapi_dapr.py <service_name>`
4. Integrate with Dapr for state management and pub/sub

## Prerequisites
- Kubernetes cluster
- Dapr installed on cluster
- Helm 3.x
- kubectl configured

## Expected Components
- FastAPI application container
- Dapr sidecar
- Service for network access
- ConfigMap for Dapr configuration

## Validation
- [ ] FastAPI service responds to health check
- [ ] Dapr sidecar running alongside service
- [ ] Service can interact with Dapr components
- [ ] Proper logging and monitoring configured

See [REFERENCE.md](./REFERENCE.md) for advanced configuration options.