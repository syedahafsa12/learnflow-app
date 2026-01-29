---
name: k8s-foundation
description: Kubernetes foundation operations and health checks
---

# Kubernetes Foundation Operations

## When to Use
- User asks to check cluster health
- Setting up basic Kubernetes resources
- Verifying Kubernetes connectivity
- Installing foundational Helm charts

## Instructions
1. Check cluster status: `python scripts/check_cluster_health.py`
2. Install basic resources: `bash scripts/setup_foundation.sh`
3. Verify readiness: `python scripts/verify_readiness.py`

## Validation
- [ ] Cluster is accessible and healthy
- [ ] Core DNS and kube-proxy are running
- [ ] Nodes are ready

See [REFERENCE.md](./REFERENCE.md) for advanced configuration options.
