#!/bin/bash

# PostgreSQL Kubernetes Deployment Script
# This script deploys PostgreSQL on Kubernetes using Helm

set -e  # Exit on any error

echo "🚀 Deploying PostgreSQL on Kubernetes..."

# Add Bitnami Helm repository
echo "📦 Adding Bitnami Helm repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create postgres namespace if it doesn't exist
echo "🌐 Creating postgres namespace..."
kubectl create namespace postgres --dry-run=client -o yaml | kubectl apply -f -

# Deploy PostgreSQL with default configuration
echo "⚙️ Installing PostgreSQL chart..."
helm install postgresql bitnami/postgresql \
  --namespace postgres \
  --set auth.postgresPassword=secretpassword \
  --set auth.database=learnflow \
  --set primary.persistence.enabled=true \
  --set primary.persistence.size=8Gi \
  --set primary.resources.requests.cpu=100m \
  --set primary.resources.requests.memory=128Mi \
  --set primary.resources.limits.cpu=500m \
  --set primary.resources.limits.memory=512Mi \
  --wait \
  --timeout=10m

echo "✅ PostgreSQL deployed successfully!"
echo ""
echo "📋 PostgreSQL Connection Information:"
echo "  Host: postgresql.postgres.svc.cluster.local"
echo "  Port: 5432"
echo "  Database: learnflow"
echo "  Username: postgres"
echo "  Password: secretpassword"
echo ""
echo "💡 Note: Change the password in production environments!"
echo "   Use Kubernetes secrets for secure credential management."