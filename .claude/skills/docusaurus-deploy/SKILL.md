---
name: docusaurus-deploy
description: Create and deploy Docusaurus documentation sites to Kubernetes
---

# Docusaurus Documentation Deployment

## When to Use
- Creating documentation sites for projects
- Deploying Docusaurus sites to Kubernetes
- Generating API documentation
- Creating knowledge bases for AI agents

## Instructions
1. Deploy Docusaurus: `./scripts/deploy.sh <site_name> <namespace>`
2. Initialize site if needed: `npx create-docusaurus@latest <site_name> classic`
3. Customize configuration: `./templates/docusaurus.config.js`
4. Verify deployment: Check site accessibility and content

## Prerequisites
- Kubernetes cluster
- Node.js and npm installed
- kubectl configured

## Expected Components
- Docusaurus application container
- Static site served by web server
- Kubernetes Deployment and Service
- Optional Ingress for external access

## LearnFlow Documentation Structure
- API documentation (auto-generated from OpenAPI)
- Skill usage guide
- Architecture overview
- Development guide
- Deployment instructions

## Validation
- [ ] Docusaurus site builds successfully
- [ ] Site is accessible via Kubernetes service
- [ ] All pages render correctly
- [ ] Search functionality works

See [REFERENCE.md](./REFERENCE.md) for customization options and plugins.