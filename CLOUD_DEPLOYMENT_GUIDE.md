# Cloud Deployment & Continuous Delivery Guide for LearnFlow

This document provides a comprehensive guide for deploying LearnFlow to cloud platforms and setting up continuous delivery with Argo CD and GitHub Actions.

## 🚀 Cloud Deployment Options

LearnFlow can be deployed to multiple cloud platforms. Choose one of the following:

### Option 1: Azure Kubernetes Service (AKS)

**Prerequisites:**
- Azure CLI installed (`az`)
- Kubernetes CLI (`kubectl`)
- Helm 3.x

**Deployment Steps:**
```bash
# Navigate to deployment scripts
cd cloud-deployment/azure/

# Make script executable
chmod +x deploy-to-azure.sh

# Run deployment
./deploy-to-azure.sh
```

**Services Used:**
- AKS: Kubernetes orchestration
- Azure Event Hubs: Messaging (replaces Kafka)
- Azure Database for PostgreSQL: Database
- Azure Monitor: Logging and metrics

### Option 2: Google Kubernetes Engine (GKE)

**Prerequisites:**
- Google Cloud SDK (`gcloud`)
- Kubernetes CLI (`kubectl`)
- Helm 3.x

**Deployment Steps:**
```bash
# Navigate to deployment scripts
cd cloud-deployment/gcp/

# Make script executable
chmod +x deploy-to-gcp.sh

# Run deployment
./deploy-to-gcp.sh
```

**Services Used:**
- GKE: Kubernetes orchestration
- Google Cloud Pub/Sub: Messaging (replaces Kafka)
- Google Cloud SQL: Database
- Google Cloud Operations Suite: Monitoring

### Option 3: Oracle Container Engine (OKE)

**Prerequisites:**
- Oracle Cloud Infrastructure CLI (`oci`)
- Kubernetes CLI (`kubectl`)
- Helm 3.x

**Deployment Steps:**
```bash
# Navigate to deployment scripts
cd cloud-deployment/oracle/

# Make script executable
chmod +x deploy-to-oracle.sh

# Run deployment
./deploy-to-oracle.sh
```

**Services Used:**
- OKE: Kubernetes orchestration
- Oracle Streaming Service: Messaging (replaces Kafka)
- Oracle Autonomous Database: Database
- OCI Monitoring: Metrics and logging

## 🔄 Continuous Deployment with Argo CD

LearnFlow uses GitOps methodology with Argo CD for continuous deployment.

### Argo CD Architecture

```
┌─────────────────┐    Sync    ┌──────────────────┐    Deploy    ┌─────────────────┐
│   Git Repo      │ ─────────▶ │   Argo CD        │ ──────────▶ │ Kubernetes      │
│  (GitHub)       │             │  Controller      │              │   Cluster       │
│                 │ ◀────────── │   (runs in K8s)  │ ◀────────── │                 │
│ • app manifests │   Status    │ • monitors apps  │   Events    │ • LearnFlow app │
│ • kustomize     │             │ • syncs changes  │             │ • configmaps    │
│ • helm charts   │             │ • health checks  │             │ • deployments   │
└─────────────────┘             └──────────────────┘             └─────────────────┘
```

### Argo CD Applications

1. **learnflow** - Main application with 6 microservices
2. **kafka-infrastructure** - Messaging infrastructure

### Installation Steps

```bash
# 1. Install Argo CD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 2. Wait for Argo CD to be ready
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# 3. Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# 4. Apply Argo CD applications
kubectl apply -f argocd/application.yaml
kubectl apply -f argocd/kafka-application.yaml

# 5. Access Argo CD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

## 🚢 GitHub Actions CI/CD Pipeline

The CI/CD pipeline automates the build and deployment process:

### Workflow Steps

1. **Build & Push** - Builds Docker images for all microservices
2. **Update Manifests** - Updates image tags in K8s manifests
3. **Argo CD Sync** - Argo CD automatically deploys changes

### Trigger Conditions

- Push to `main` branch
- Pull requests to `main` branch

### GitHub Actions Configuration

```yaml
# .github/workflows/ci-cd.yaml
name: LearnFlow CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# Builds images for all 6 microservices
# Updates manifests with new image tags
# Argo CD automatically syncs to cluster
```

## 📋 Deployment Validation

After deployment, verify the following:

### 1. Check Argo CD Applications
```bash
kubectl get applications -n argocd
```

Expected output:
```
NAME                    SYNC STATUS   HEALTH STATUS
learnflow               Synced        Healthy
kafka-infrastructure    Synced        Healthy
```

### 2. Check LearnFlow Services
```bash
kubectl get pods -n learnflow
```

Expected: All 6 microservices running with Dapr sidecars

### 3. Check External Access
```bash
kubectl get svc frontend -n learnflow
```

Expected: External IP assigned for frontend access

### 4. Verify Dapr Sidecars
```bash
kubectl get pods -n learnflow -o yaml | grep dapr
```

Expected: Dapr sidecars injected in all microservice pods

## 🔧 Configuration Management

### Environment Variables

Configuration is managed through Kubernetes ConfigMaps and Secrets:

- **Database**: PostgreSQL connection details
- **Messaging**: Kafka/Event Hub connection strings
- **Dapr**: Component configurations
- **Monitoring**: Metrics and logging endpoints

### Infrastructure as Code

All infrastructure is defined in:

- `k8s/` - Kubernetes manifests
- `cloud-deployment/` - Cloud-specific configurations
- `argocd/` - GitOps applications
- `.github/workflows/` - CI/CD pipelines

## 🧪 Testing in Production

### Health Checks

Each microservice has health endpoints:
- `/health` - Basic health check
- `/dapr/healthz` - Dapr sidecar health

### Monitoring

- **Metrics**: Prometheus + Grafana (planned)
- **Logs**: Cloud-native logging solutions
- **Tracing**: Dapr distributed tracing

## 🔐 Security Considerations

### Network Security

- Namespaces isolate components
- Network policies restrict traffic
- TLS encryption for all communication

### Secrets Management

- Kubernetes secrets for sensitive data
- Cloud KMS integration (when using managed services)
- Dapr secrets management

## 📊 Scaling Guidelines

### Horizontal Pod Autoscaling

Based on CPU and memory usage:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
# Applied to all microservices
```

### Dapr Scaling

- Sidecar resources configurable
- State store partitioning
- Pub/Sub message queuing

## 🔄 Rollback Strategy

### GitOps Rollback

1. Revert Git commit in main branch
2. Argo CD automatically syncs the rollback
3. Kubernetes performs rolling update to previous version

### Manual Override

```bash
# Rollback specific application
argocd app rollback learnflow <revision-number>

# Force sync to desired state
argocd app sync learnflow --force
```

## 🚨 Troubleshooting

### Common Issues

1. **ImagePullBackOff**: Check image registry access
2. **CrashLoopBackOff**: Check resource limits and dependencies
3. **OutOfSync**: Verify Git repository permissions

### Debug Commands

```bash
# Check Argo CD controller logs
kubectl logs -n argocd deployment/argocd-application-controller

# Compare live vs desired state
argocd app diff learnflow

# Get detailed application status
kubectl describe application learnflow -n argocd
```

## 📈 Performance Optimization

### Resource Optimization

- CPU/Memory requests and limits set appropriately
- Dapr sidecar resource allocation optimized
- Database connection pooling configured

### Network Optimization

- Service mesh routing optimized
- Load balancing configured for external access
- CDN integration for static assets (frontend)

## 🎯 Next Steps

### Post-Deployment

1. Set up monitoring and alerting
2. Configure SSL certificates for HTTPS
3. Set up backup and disaster recovery
4. Performance testing and optimization

### Advanced Features

1. Progressive delivery with Argo Rollouts
2. Multi-region deployment
3. Advanced security policies
4. Cost optimization strategies

## 📚 Resources

- [Argo CD Documentation](https://argo-cd.readthedocs.io/)
- [Dapr Documentation](https://dapr.io/)
- [Kubernetes Documentation](https://kubernetes.io/)
- [Cloud Provider Documentation](https://cloud.google.com/gke/docs)

---

**LearnFlow** is now ready for production deployment across multiple cloud platforms with automated continuous delivery!