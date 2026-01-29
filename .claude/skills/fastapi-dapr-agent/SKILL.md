---
name: fastapi-dapr-agent
description: Create FastAPI microservices with Dapr for AI agents
---

# FastAPI Dapr Agent Service Creator

## When to Use
- User asks to create a new microservice
- Need to implement AI agent as a service
- Building event-driven microservices with Dapr
- Creating API endpoints with FastAPI

## Instructions
1. Create service: `bash scripts/create_service.sh <service_name>`
2. Add Dapr configuration: `bash scripts/add_dapr_config.sh <service_name>`
3. Deploy to Kubernetes: `bash scripts/deploy_to_k8s.sh <service_name>`
4. Verify deployment: `python scripts/verify_deployment.py <service_name>`

## Validation
- [ ] Service runs successfully
- [ ] Dapr sidecar is attached
- [ ] Service is accessible via Kubernetes

See [REFERENCE.md](./REFERENCE.md) for configuration options and [templates/](./templates/) for available templates.
