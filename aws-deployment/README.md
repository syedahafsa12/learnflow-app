# LearnFlow AWS Deployment Guide

This directory contains all AWS deployment configurations for the LearnFlow AI tutoring platform.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         AWS Cloud                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  Amazon EKS Cluster                  │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  LearnFlow Namespace                         │   │  │
│  │  │  - Triage Agent (FastAPI + Dapr)            │   │  │
│  │  │  - Concepts Agent (FastAPI + Dapr)          │   │  │
│  │  │  - Code Review Agent (FastAPI + Dapr)       │   │  │
│  │  │  - Debug Agent (FastAPI + Dapr)             │   │  │
│  │  │  - Next.js Frontend                         │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Infrastructure Namespace                    │   │  │
│  │  │  - Kafka (3 brokers)                        │   │  │
│  │  │  - PostgreSQL (RDS or in-cluster)          │   │  │
│  │  │  - Dapr System Components                   │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   ECR        │  │   RDS        │  │   Route 53   │    │
│  │  (Images)    │  │ (PostgreSQL) │  │    (DNS)     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

1. **AWS CLI** configured with appropriate credentials
2. **eksctl** for EKS cluster management
3. **kubectl** for Kubernetes operations
4. **Helm** for package management
5. **Docker** for building images

## Deployment Steps

### Step 1: Create EKS Cluster

```bash
eksctl create cluster -f aws-deployment/eks-cluster.yaml
```

### Step 2: Configure kubectl

```bash
aws eks update-kubeconfig --name learnflow-cluster --region us-east-1
```

### Step 3: Install Dapr on EKS

```bash
dapr init -k
```

### Step 4: Deploy PostgreSQL (Choose Option A or B)

**Option A: Amazon RDS (Recommended for Production)**
```bash
terraform apply -f aws-deployment/terraform/rds/
```

**Option B: In-Cluster PostgreSQL**
```bash
bash .claude/skills/postgres-k8s-setup/scripts/deploy_postgres.sh
```

### Step 5: Deploy Kafka

```bash
bash .claude/skills/kafka-k8s-setup/scripts/deploy_kafka.sh
```

### Step 6: Build and Push Images to ECR

```bash
bash aws-deployment/scripts/build-and-push-ecr.sh
```

### Step 7: Deploy Microservices

```bash
kubectl apply -f aws-deployment/manifests/
```

### Step 8: Deploy Frontend

```bash
bash .claude/skills/nextjs-k8s-deploy/scripts/build_deploy.sh learnflow-frontend learnflow
```

### Step 9: Configure Ingress/Load Balancer

```bash
kubectl apply -f aws-deployment/manifests/ingress.yaml
```

### Step 10: Setup CI/CD with ArgoCD

```bash
kubectl apply -f aws-deployment/argocd/
```

## Cost Optimization

- **EKS Control Plane**: ~$73/month
- **Worker Nodes**: 3x t3.medium = ~$75/month
- **RDS PostgreSQL**: t3.micro = ~$15/month
- **Load Balancer**: ~$20/month
- **ECR Storage**: ~$5/month

**Total Estimated Cost**: ~$188/month

### Free Tier Eligible

Many services have free tier for first 12 months:
- 750 hours of t3.micro RDS
- 5 GB ECR storage
- AWS Free Tier eligible

## Monitoring & Observability

- **CloudWatch** for logs and metrics
- **Prometheus + Grafana** for Kubernetes monitoring
- **Dapr Dashboard** for service mesh observability
- **X-Ray** for distributed tracing

## Security

- **IAM Roles** for service accounts (IRSA)
- **AWS Secrets Manager** for credentials
- **Network Policies** for pod-to-pod communication
- **TLS/SSL** via AWS Certificate Manager

## Scaling

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: triage-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: triage-agent
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Cluster Autoscaler
```bash
kubectl apply -f aws-deployment/manifests/cluster-autoscaler.yaml
```

## Disaster Recovery

- **RDS Automated Backups**: Daily snapshots
- **Velero** for Kubernetes backup
- **Multi-AZ** deployment for high availability

## Next Steps

1. Configure custom domain in Route 53
2. Setup SSL certificates via ACM
3. Configure CloudFront CDN for frontend
4. Enable auto-scaling policies
5. Setup monitoring alerts

## Troubleshooting

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues and solutions.
