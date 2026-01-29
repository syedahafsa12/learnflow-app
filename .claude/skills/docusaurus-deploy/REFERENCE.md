# Docusaurus Deployment Reference

## Purpose
The Docusaurus Deployment skill creates and deploys documentation sites to Kubernetes, optimized for the LearnFlow platform documentation.

## Features
- Docusaurus site scaffolding
- Custom LearnFlow theming
- Docker image building
- Kubernetes deployment
- Site verification

## Usage Patterns
### Basic Deployment
```bash
bash scripts/deploy.sh <site_name>
```

### Site Configuration
```bash
bash scripts/configure_site.sh <site_name>
```

### Verification
```bash
python scripts/verify_deployment.py <site_name>
```

## Configuration Options
- Customize site configuration in docusaurus.config.js
- Adjust replica counts in deployment.yaml
- Modify resource limits
- Update branding and styling

## LearnFlow Documentation Structure
The skill creates documentation sections for:
- Getting Started guides
- Service documentation
- AI Agent guides
- Infrastructure components
- API references
- Troubleshooting

## Dependencies
- Node.js 18+
- Docker
- Kubernetes cluster
- kubectl
- npx

## Best Practices
- Use static site generation for performance
- Implement proper caching headers
- Optimize for SEO
- Include search functionality
- Provide clear navigation

## Integration with AI Agents
- Claude Code can generate documentation sites
- Goose can manage deployments and verify sites
- Enables comprehensive documentation for LearnFlow
