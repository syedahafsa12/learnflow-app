# Next.js Kubernetes Deployment Reference

## Purpose
The Next.js Kubernetes Deployment skill builds and deploys Next.js applications to Kubernetes with optimized configurations for the LearnFlow platform.

## Features
- Next.js application scaffolding
- Docker image building
- Kubernetes deployment manifests
- Environment configuration
- Application verification

## Usage Patterns
### Basic Deployment
```bash
bash scripts/build_deploy.sh <app_name>
```

### Environment Configuration
```bash
bash scripts/configure_env.sh <app_name>
```

### Verification
```bash
python scripts/verify_deployment.py <app_name>
```

## Configuration Options
- Adjust replica counts in deployment.yaml
- Modify resource limits
- Customize environment variables
- Change Docker build settings

## LearnFlow Frontend Components
The skill creates a Next.js application with:
- App Router structure
- Tailwind CSS styling
- Monaco Editor integration
- Better Auth authentication
- Responsive design
- API integration capabilities

## Dependencies
- Node.js 18+
- Docker
- Kubernetes cluster
- kubectl
- npx

## Best Practices
- Use multi-stage Docker builds for optimized images
- Implement proper health checks
- Configure appropriate resource limits
- Set up proper environment variables
- Enable gzip compression

## Integration with AI Agents
- Claude Code can deploy Next.js apps with single command
- Goose can manage configurations and verify deployments
- Enables rapid frontend development for LearnFlow
