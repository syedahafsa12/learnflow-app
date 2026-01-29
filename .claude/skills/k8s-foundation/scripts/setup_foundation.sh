#!/bin/bash

# Kubernetes Foundation Setup
# Installs basic resources and configurations needed for a cluster

set -e  # Exit on any error

echo "Setting up Kubernetes foundation..."

# Update Helm repositories
echo "Updating Helm repositories..."
helm repo update

# Create namespaces if they don't exist
echo "Creating essential namespaces..."
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace logging --dry-run=client -o yaml | kubectl apply -f -

# Check if ingress-nginx is available and install if needed
if ! kubectl get namespace ingress-nginx >/dev/null 2>&1; then
    echo "Installing ingress-nginx controller..."
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
fi

# Verify installation
echo "Verifying installations..."
kubectl get namespaces
kubectl get pods --all-namespaces | grep -E "(ingress|monitoring|logging)"

echo "✓ Kubernetes foundation setup complete!"
