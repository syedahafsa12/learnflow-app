#!/bin/bash

# Simple Kafka Deployment Script for Minikube
# Deploys Apache Kafka using a simplified approach

set -e  # Exit on any error

echo "Deploying Apache Kafka to Kubernetes..."

# Add and update Helm repositories
echo "Adding Confluentinc repository..."
helm repo add confluentinc https://confluentinc.github.io/cp-helm-charts/
helm repo update

# Create kafka namespace if it doesn't exist
echo "Creating kafka namespace..."
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

# Install Kafka using Helm with simplified configuration
echo "Installing Kafka..."
helm install kafka confluentinc/cp-kafka \
  --namespace kafka \
  --set cp-zookeeper.enabled=true \
  --set cp-kafka.enabled=true \
  --set cp-kafka.replicas=1 \
  --set cp-zookeeper.replicas=1 \
  --set cp-kafka.heapOptions="-Xmx512m -Xms512m" \
  --set cp-zookeeper.heapOptions="-Xmx512m -Xms512m" \
  --wait \
  --timeout=10m

# Wait for pods to be ready
echo "Waiting for Kafka pods to be ready..."
kubectl wait --for=condition=ready pod -l app=cp-kafka -n kafka --timeout=300s || true
kubectl wait --for=condition=ready pod -l app=cp-zookeeper -n kafka --timeout=300s || true

echo "✓ Kafka deployed successfully to namespace 'kafka'"
