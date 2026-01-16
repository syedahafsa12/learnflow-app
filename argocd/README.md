# Argo CD GitOps Configuration for LearnFlow

## Overview

This directory contains Argo CD Application manifests for continuous deployment of LearnFlow using the GitOps approach.

## Architecture

```
GitHub Repository (Source of Truth)
         |
         | Git Push (triggers GitHub Actions)
         v
   GitHub Actions CI/CD
         |
         | Build Docker images
         | Push to ghcr.io
         | Update K8s manifests
         v
   Git Repository Updated
         |
         | Argo CD watches repository
         v
   Argo CD Application
         |
         | Automatic sync
         v
   Kubernetes Cluster
```

## Applications

### 1. learnflow (Main Application)
- **Path:** `k8s/`
- **Namespace:** `learnflow`
- **Components:** 6 microservices with Dapr sidecars
- **Auto-sync:** Enabled with self-heal and pruning

### 2. kafka-infrastructure
- **Path:** `k8s/` (filtered: `kafka-*.yaml`)
- **Namespace:** `kafka`
- **Components:** Kafka topics configuration
- **Auto-sync:** Enabled

## Installation

### Prerequisites
```bash
# Install Argo CD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for Argo CD to be ready
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Deploy Applications
```bash
# Apply LearnFlow application
kubectl apply -f argocd/application.yaml

# Apply Kafka infrastructure
kubectl apply -f argocd/kafka-application.yaml

# Access Argo CD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Open: https://localhost:8080
# Username: admin
# Password: [from previous command]
```

## GitOps Workflow

### 1. Make Code Changes
```bash
# Edit code in backend/
git add .
git commit -m "feat: add new feature"
git push origin main
```

### 2. GitHub Actions Triggers
- Builds Docker images for all services
- Pushes images to GitHub Container Registry
- Updates image tags in `k8s/*.yaml` manifests
- Commits changes back to repository

### 3. Argo CD Syncs
- Detects manifest changes in Git
- Automatically syncs to Kubernetes cluster
- Self-heals if manual changes occur
- Prunes deleted resources

### 4. Verify Deployment
```bash
# Check Argo CD application status
kubectl get applications -n argocd

# Check LearnFlow pods
kubectl get pods -n learnflow

# View sync history
argocd app history learnflow
```

## Configuration Options

### Sync Policy
```yaml
syncPolicy:
  automated:
    prune: true        # Delete resources not in Git
    selfHeal: true     # Revert manual changes
    allowEmpty: false  # Prevent empty syncs
```

### Retry Strategy
```yaml
retry:
  limit: 5              # Max retry attempts
  backoff:
    duration: 5s        # Initial delay
    factor: 2           # Backoff multiplier
    maxDuration: 3m     # Max delay between retries
```

## Monitoring

### View Application Status
```bash
# CLI
argocd app get learnflow

# Web UI
# Navigate to Applications → learnflow
```

### View Sync Logs
```bash
argocd app logs learnflow --follow
```

### Manual Sync (if needed)
```bash
argocd app sync learnflow
```

## Rollback

### Rollback to Previous Version
```bash
# View history
argocd app history learnflow

# Rollback to specific revision
argocd app rollback learnflow <revision-number>
```

### Rollback via Git
```bash
# Revert Git commit
git revert <commit-hash>
git push origin main

# Argo CD will automatically sync the rollback
```

## Troubleshooting

### Application Not Syncing
```bash
# Check application status
kubectl describe application learnflow -n argocd

# Check Argo CD logs
kubectl logs -n argocd deployment/argocd-application-controller
```

### Sync Errors
```bash
# View sync errors
argocd app get learnflow

# Force sync
argocd app sync learnflow --force
```

### OutOfSync Status
```bash
# Compare live vs desired state
argocd app diff learnflow

# Refresh application
argocd app get learnflow --refresh
```

## Best Practices

1. **Never edit resources directly** - Always commit to Git
2. **Use branches** for testing changes before merging to main
3. **Monitor sync status** regularly via Argo CD UI
4. **Set up notifications** for sync failures (Slack, email)
5. **Use AppProjects** to control permissions and allowed resources

## Security

### Repository Access
- Argo CD uses GitHub token for repository access
- Configure in Argo CD: Settings → Repositories

### RBAC
```yaml
# Limit user permissions
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.default: role:readonly
```

## Integration with GitHub Actions

The `.github/workflows/ci-cd.yaml` workflow:
1. Builds Docker images on every push to `main`
2. Updates image tags in K8s manifests
3. Commits changes back to repository
4. Argo CD detects changes and syncs automatically

## Next Steps

1. Set up Argo CD notifications
2. Configure SSO for Argo CD UI
3. Add progressive delivery with Argo Rollouts
4. Set up monitoring with Prometheus/Grafana

## Resources

- [Argo CD Documentation](https://argo-cd.readthedocs.io/)
- [GitOps Principles](https://www.gitops.tech/)
- [Argo CD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
