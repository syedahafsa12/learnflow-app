---
name: docusaurus-deploy
description: Deploy Docusaurus documentation sites to Kubernetes
---

# Docusaurus Deployment

## When to Use
- User asks to create documentation site
- Need to deploy Docusaurus for LearnFlow
- Setting up documentation for AI agents

## Instructions
1. Create site: `bash scripts/deploy.sh <site_name>`
2. Configure site: `bash scripts/configure_site.sh <site_name>`
3. Build and deploy: `bash scripts/build_and_deploy.sh <site_name>`
4. Verify deployment: `python scripts/verify_deployment.py <site_name>`

## Validation
- [ ] Docusaurus site is created
- [ ] Site builds successfully
- [ ] Kubernetes deployment is created
- [ ] Documentation is accessible

See [REFERENCE.md](./REFERENCE.md) for customization options.
