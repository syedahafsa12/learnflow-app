#!/bin/bash

# PostgreSQL Kubernetes Deployment Script
# Deploys PostgreSQL using Bitnami Helm chart

set -e  # Exit on any error

echo "Deploying PostgreSQL to Kubernetes..."

# Add and update Helm repositories
echo "Adding Bitnami repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create postgresql namespace if it doesn't exist
echo "Creating postgresql namespace..."
kubectl create namespace postgresql --dry-run=client -o yaml | kubectl apply -f -

# Set up default credentials
POSTGRES_USER=${POSTGRES_USER:-"learnflow"}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-"learnflow123"}
POSTGRES_DB=${POSTGRES_DB:-"learnflow_db"}

# Install PostgreSQL using Helm
echo "Installing PostgreSQL..."
helm install postgresql bitnami/postgresql \
  --namespace postgresql \
  --set auth.postgresPassword="$POSTGRES_PASSWORD" \
  --set auth.database="$POSTGRES_DB" \
  --set auth.username="$POSTGRES_USER" \
  --set auth.password="$POSTGRES_PASSWORD" \
  --set primary.persistence.enabled=false \
  --set image.debug=true \
  --wait \
  --timeout=10m

# Wait for pod to be ready
echo "Waiting for PostgreSQL pod to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=postgresql -n postgresql --timeout=300s

# Expose PostgreSQL service internally
kubectl patch svc postgresql -n postgresql -p '{"spec":{"type":"ClusterIP"}}'

echo "✓ PostgreSQL deployed successfully to namespace 'postgresql'"
echo "Database: $POSTGRES_DB"
echo "Username: $POSTGRES_USER"
echo "Password: $POSTGRES_PASSWORD"
