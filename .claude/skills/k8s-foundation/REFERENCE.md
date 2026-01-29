# Kubernetes Foundation Reference

## Purpose
The Kubernetes Foundation skill provides essential operations for managing and verifying Kubernetes cluster health and readiness.

## Features
- Cluster health checking
- Foundation component installation
- Readiness verification
- Resource capacity assessment

## Usage Patterns
### Health Check
```bash
python scripts/check_cluster_health.py
```

### Foundation Setup
```bash
bash scripts/setup_foundation.sh
```

### Readiness Verification
```bash
python scripts/verify_readiness.py
```

## Configuration Options
- Modify namespace creation in setup_foundation.sh
- Adjust readiness thresholds in verify_readiness.py
- Customize health check criteria in check_cluster_health.py

## Dependencies
- kubectl
- Helm
- Kubernetes cluster access

## Best Practices
- Run health checks regularly
- Verify readiness before deploying applications
- Monitor resource capacity for scaling decisions
- Check component statuses during troubleshooting

## Integration with AI Agents
- Claude Code can use this for cluster management
- Goose can leverage this for infrastructure operations
- Provides consistent cluster verification across tools
