---
name: nextjs-k8s-deploy
description: Build and deploy Next.js applications to Kubernetes with optimized Docker images
---

# Next.js Kubernetes Deployment

## When to Use
- Deploying Next.js applications to Kubernetes
- Creating optimized Docker images for Next.js
- Setting up production-ready Next.js deployments
- Deploying LearnFlow frontend with Monaco editor

## Instructions
1. Build and deploy: `./scripts/build_deploy.sh <app_name> <namespace>`
2. Create optimized Dockerfile: `./templates/Dockerfile.nextjs`
3. Deploy to K8s: Creates deployment, service, ingress
4. Verify deployment: `python scripts/verify_nextjs.py <app_name> <namespace>`

## Prerequisites
- Kubernetes cluster
- Docker daemon running
- kubectl configured
- Helm (optional for advanced deployments)

## Expected Components
- Next.js application container
- Optimized multi-stage Docker build
- Kubernetes Deployment
- Service for network access
- Ingress for external access (optional)

## LearnFlow Frontend Features
- Next.js 14+ with App Router
- Monaco Editor for code editing
- TailwindCSS for styling
- Better Auth for authentication
- Responsive design for all devices

## Validation
- [ ] Next.js application responds to requests
- [ ] Docker build completes successfully
- [ ] Kubernetes resources created properly
- [ ] Health checks passing

See [REFERENCE.md](./REFERENCE.md) for optimization techniques and environment variables.