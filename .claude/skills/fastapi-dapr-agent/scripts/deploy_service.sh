#!/bin/bash
set -e

SERVICE_NAME=$1
NAMESPACE=${2:-default}
IMAGE_NAME=${3:-$SERVICE_NAME}
IMAGE_TAG=${4:-latest}

if [ -z "$SERVICE_NAME" ]; then
    echo "Usage: ./deploy_service.sh <service_name> [namespace] [image_name] [image_tag]"
    exit 1
fi

echo "Deploying $SERVICE_NAME to Kubernetes with Dapr..."

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Create Kubernetes manifests
cat > /tmp/${SERVICE_NAME}-deployment.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${SERVICE_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${SERVICE_NAME}
  template:
    metadata:
      labels:
        app: ${SERVICE_NAME}
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "${SERVICE_NAME}"
        dapr.io/app-port: "8000"
        dapr.io/enable-api-logging: "true"
    spec:
      containers:
      - name: ${SERVICE_NAME}
        image: ${IMAGE_NAME}:${IMAGE_TAG}
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
        env:
        - name: SERVICE_NAME
          value: "${SERVICE_NAME}"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: ${SERVICE_NAME}
  namespace: ${NAMESPACE}
spec:
  selector:
    app: ${SERVICE_NAME}
  ports:
  - port: 8000
    targetPort: 8000
    protocol: TCP
  type: ClusterIP
EOF

# Apply manifests
kubectl apply -f /tmp/${SERVICE_NAME}-deployment.yaml

echo "✓ ${SERVICE_NAME} deployed with Dapr sidecar"
echo "  Namespace: ${NAMESPACE}"
echo "  Dapr App ID: ${SERVICE_NAME}"
