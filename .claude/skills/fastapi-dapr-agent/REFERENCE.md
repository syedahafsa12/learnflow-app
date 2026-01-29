# FastAPI Dapr Agent Service Reference

## Purpose
The FastAPI Dapr Agent Service skill creates, configures, and deploys AI-enabled microservices with Dapr integration for the LearnFlow platform.

## Features
- FastAPI service scaffolding
- Dapr sidecar integration
- Kubernetes deployment
- State management and pub/sub patterns
- Health checks and verification

## Usage Patterns
### Create New Service
```bash
bash scripts/create_service.sh <service_name>
```

### Add Dapr Configuration
```bash
bash scripts/add_dapr_config.sh <service_name>
```

### Deploy to Kubernetes
```bash
bash scripts/deploy_to_k8s.sh <service_name>
```

### Verify Deployment
```bash
python scripts/verify_deployment.py <service_name>
```

## Configuration Options
- Modify service templates in templates/ directory
- Adjust Dapr components in add_dapr_config.sh
- Customize Kubernetes manifests in deploy_to_k8s.sh
- Update dependencies in requirements.txt

## LearnFlow AI Agents
The skill supports creating these AI agents for LearnFlow:
- `triage-agent` - Routes queries to appropriate specialists
- `concepts-agent` - Explains Python concepts with examples
- `code-review-agent` - Reviews student code for quality
- `debug-agent` - Helps students debug errors
- `exercise-agent` - Generates coding challenges
- `progress-agent` - Tracks student mastery

## Dependencies
- Kubernetes cluster
- Dapr installed on cluster
- Docker
- kubectl
- Python 3.7+

## Best Practices
- Use meaningful service names
- Implement proper error handling
- Leverage Dapr for state management
- Follow FastAPI best practices
- Test locally before deploying

## Integration with AI Agents
- Claude Code can create services with single command
- Goose can manage deployments and configurations
- Enables rapid AI agent development and deployment
