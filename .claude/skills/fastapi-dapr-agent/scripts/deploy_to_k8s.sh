#!/bin/bash

# FastAPI Dapr Service Kubernetes Deployment Script
# Builds and deploys a FastAPI service with Dapr to Kubernetes

set -e  # Exit on any error

if [ $# -eq 0 ]; then
    echo "Usage: $0 <service_name>"
    exit 1
fi

SERVICE_NAME=$1
SERVICE_DIR="./${SERVICE_NAME}"
IMAGE_NAME="learnflow-$SERVICE_NAME:latest"

echo "Building and deploying $SERVICE_NAME to Kubernetes..."

# Build Docker image
echo "Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" "$SERVICE_DIR"

# Tag for minikube
eval $(minikube docker-env)
docker tag "$IMAGE_NAME" "$IMAGE_NAME"

# Create Kubernetes manifests
MANIFEST_DIR="./k8s-manifests-$SERVICE_NAME"
mkdir -p "$MANIFEST_DIR"

# Create Deployment with Dapr sidecar
cat > "$MANIFEST_DIR/deployment.yaml" << DEPLOYMENT_EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $SERVICE_NAME
  labels:
    app: $SERVICE_NAME
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $SERVICE_NAME
  template:
    metadata:
      labels:
        app: $SERVICE_NAME
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "$SERVICE_NAME"
        dapr.io/app-port: "8000"
        dapr.io/app-protocol: "http"
        dapr.io/log-level: "info"
        dapr.io/sidecar-listen-addresses: "0.0.0.0"
    spec:
      containers:
      - name: $SERVICE_NAME
        image: $IMAGE_NAME
        ports:
        - containerPort: 8000
        env:
        - name: PORT
          value: "8000"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
DEPLOYMENT_EOF

# Create Service
cat > "$MANIFEST_DIR/service.yaml" << SERVICE_EOF
apiVersion: v1
kind: Service
metadata:
  name: $SERVICE_NAME-service
  labels:
    app: $SERVICE_NAME
spec:
  selector:
    app: $SERVICE_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
SERVICE_EOF

# Apply the manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f "$MANIFEST_DIR/"

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/$SERVICE_NAME --timeout=300s

# Get the service external IP
echo "Getting service information..."
kubectl get svc $SERVICE_NAME-service

echo "✓ Service $SERVICE_NAME deployed successfully to Kubernetes!"
echo "Deployment name: $SERVICE_NAME"
echo "Service name: $SERVICE_NAME-service"
