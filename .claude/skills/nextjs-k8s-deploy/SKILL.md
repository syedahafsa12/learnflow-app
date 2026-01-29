---
name: nextjs-k8s-deploy
description: Deploy Next.js applications to Kubernetes
---

# Next.js Kubernetes Deployment

## When to Use
- User asks to deploy Next.js application
- Need to create frontend for LearnFlow
- Deploying React applications with Monaco Editor

## Instructions
1. Build and deploy: `bash scripts/build_deploy.sh <app_name>`
2. Configure environment: `bash scripts/configure_env.sh <app_name>`
3. Verify deployment: `python scripts/verify_deployment.py <app_name>`
4. Confirm application is accessible.

## Validation
- [ ] Next.js app builds successfully
- [ ] Kubernetes deployment is created
- [ ] Application is accessible via browser

See [REFERENCE.md](./REFERENCE.md) for configuration options.
