#!/bin/bash

# Kafka Kubernetes Deployment Script
# This script deploys Apache Kafka on Kubernetes using Helm

set -e  # Exit on any error

echo "🚀 Deploying Kafka on Kubernetes..."

# Add Bitnami Helm repository
echo "📦 Adding Bitnami Helm repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create kafka namespace if it doesn't exist
echo "🌐 Creating kafka namespace..."
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

# Deploy Kafka with default configuration
echo "⚙️ Installing Kafka chart..."
helm install kafka bitnami/kafka \
  --namespace kafka \
  --set replicaCount=1 \
  --set zookeeper.enabled=true \
  --set zookeeper.replicaCount=1 \
  --set service.type=ClusterIP \
  --wait \
  --timeout=10m

echo "✅ Kafka deployed successfully!"
echo ""
echo "📋 Kafka Connection Information:"
echo "  Namespace: kafka"
echo "  Service: kafka"
echo "  Port: 9092"
echo ""
echo "💡 To connect to Kafka externally, you may need to create a port forward:"
echo "   kubectl port-forward -n kafka svc/kafka 9092:9092"