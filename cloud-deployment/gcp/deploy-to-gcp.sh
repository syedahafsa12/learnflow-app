#!/bin/bash

# Deploy LearnFlow to Google Kubernetes Engine (GKE)
# This script automates the deployment process to Google Cloud

set -e  # Exit on any error

echo "🚀 Deploying LearnFlow to Google Kubernetes Engine..."

# Check if Google Cloud SDK is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK is not installed. Please install it first."
    echo "Installation: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install it first."
    exit 1
fi

# Login to Google Cloud (you may need to authenticate)
echo "🔐 Authenticating with Google Cloud..."
gcloud auth login

# Set your project
echo "💳 Setting Google Cloud project..."
read -p "Enter your Google Cloud Project ID: " GCLOUD_PROJECT_ID
gcloud config set project $GCLOUD_PROJECT_ID

# Enable required APIs
echo "🔌 Enabling required APIs..."
gcloud services enable container.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable pubsub.googleapis.com

# Create GKE cluster
echo "🐳 Creating GKE cluster..."
read -p "Enter GKE cluster name (default: learnflow-gke): " GKE_CLUSTER_NAME
GKE_CLUSTER_NAME=${GKE_CLUSTER_NAME:-"learnflow-gke"}
ZONE=${ZONE:-"us-central1-a"}

gcloud container clusters create $GKE_CLUSTER_NAME \
    --zone=$ZONE \
    --num-nodes=3 \
    --enable-autorepair \
    --enable-autoupgrade \
    --machine-type=e2-standard-2

# Get GKE credentials
echo "🔑 Getting GKE credentials..."
gcloud container clusters get-credentials $GKE_CLUSTER_NAME --zone $ZONE

# Deploy Dapr to GKE
echo "⚡ Installing Dapr..."
kubectl apply -f https://raw.githubusercontent.com/dapr/dapr/v1.11.0/deployments/charts/dapr_latest_version/charts/dapr-crds/crds/all.yaml
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update
helm install dapr dapr/dapr --namespace dapr-system --create-namespace --wait

# Deploy Google Cloud managed services (instructions)
echo "☁️ Preparing for Google Cloud managed services..."
echo "Please provision these GCP services manually or via Terraform:"
echo "- Google Cloud Pub/Sub (for Kafka replacement)"
echo "- Google Cloud SQL for PostgreSQL (for database replacement)"
echo "- Configure the connection strings in your application"

# Deploy LearnFlow application
echo "🚢 Deploying LearnFlow application to GKE..."
kubectl apply -f ../../../learnflow-app/k8s/

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=triage-agent -n default --timeout=300s
kubectl wait --for=condition=ready pod -l app=concepts-agent -n default --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend -n default --timeout=300s

# Set up Cloud Load Balancer
echo "🌐 Configuring external load balancer..."
kubectl patch service frontend -p '{"spec":{"type":"LoadBalancer"}}'

# Wait for external IP
echo "⏳ Waiting for external IP assignment..."
FRONTEND_IP=""
while [ -z "$FRONTEND_IP" ]; do
    FRONTEND_IP=$(kubectl get svc frontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
    if [ -z "$FRONTEND_IP" ]; then
        echo "Waiting for external IP assignment..."
        sleep 10
    fi
done

echo "✅ LearnFlow deployed successfully to Google Cloud!"
echo "Frontend URL: http://$FRONTEND_IP"
echo ""
echo "📝 Next steps:"
echo "1. Configure Google Cloud Pub/Sub as Kafka replacement"
echo "2. Configure Google Cloud SQL for PostgreSQL"
echo "3. Update application configuration with cloud service endpoints"
echo "4. Set up Google Cloud Operations Suite for monitoring"

# Show deployment status
echo ""
echo "📋 Current deployment status:"
kubectl get pods
kubectl get services