#!/bin/bash

# Kafka Kubernetes Deployment Script
# Deploys Apache Kafka using Bitnami Helm chart
# NOTE: This script may need adjustments based on your specific Kubernetes environment

set -e  # Exit on any error

echo "Deploying Apache Kafka to Kubernetes..."

# Add and update Helm repositories
echo "Adding Bitnami repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create kafka namespace if it doesn't exist
echo "Creating kafka namespace..."
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f - --validate=false

# Install Kafka using Helm with environment-adapted settings
echo "Installing Kafka with Zookeeper (may take several minutes)..."
helm install kafka bitnami/kafka \
  --namespace kafka \
  --set replicaCount=1 \
  --set controller.replicaCount=0 \
  --set broker.replicaCount=1 \
  --set zookeeper.enabled=true \
  --set zookeeper.replicaCount=1 \
  --set auth.clientProtocol=plaintext \
  --set auth.interBrokerProtocol=plaintext \
  --set persistence.enabled=false \
  --set resources.limits.cpu=500m \
  --set resources.limits.memory=1Gi \
  --set resources.requests.cpu=250m \
  --set resources.requests.memory=512Mi \
  --wait \
  --timeout=10m

# Wait for pods to be ready
echo "Waiting for Kafka pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kafka -n kafka --timeout=300s || echo "Note: Pods may still be initializing, check with: kubectl get pods -n kafka"

echo "✓ Kafka deployment initiated in namespace 'kafka'"
echo "Check status with: kubectl get pods -n kafka"
