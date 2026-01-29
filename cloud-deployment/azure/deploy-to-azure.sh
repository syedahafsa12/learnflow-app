#!/bin/bash

# Deploy LearnFlow to Azure Kubernetes Service (AKS)
# This script automates the deployment process to Azure

set -e  # Exit on any error

echo "🚀 Deploying LearnFlow to Azure Kubernetes Service..."

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    echo "Installation: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install it first."
    exit 1
fi

# Login to Azure (you may need to authenticate)
echo "🔐 Authenticating with Azure..."
az login

# Set your subscription
echo "💳 Setting Azure subscription..."
read -p "Enter your Azure Subscription ID: " AZURE_SUBSCRIPTION_ID
az account set --subscription $AZURE_SUBSCRIPTION_ID

# Create resource group
echo "🏗️ Creating resource group..."
read -p "Enter resource group name (default: learnflow-rg): " RESOURCE_GROUP
RESOURCE_GROUP=${RESOURCE_GROUP:-"learnflow-rg"}
LOCATION=${LOCATION:-"eastus"}

az group create --name $RESOURCE_GROUP --location $LOCATION

# Create AKS cluster
echo "🐳 Creating AKS cluster..."
read -p "Enter AKS cluster name (default: learnflow-aks): " AKS_CLUSTER_NAME
AKS_CLUSTER_NAME=${AKS_CLUSTER_NAME:-"learnflow-aks"}

az aks create \
    --resource-group $RESOURCE_GROUP \
    --name $AKS_CLUSTER_NAME \
    --node-count 3 \
    --enable-addons monitoring \
    --generate-ssh-keys

# Get AKS credentials
echo "🔑 Getting AKS credentials..."
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER_NAME

# Deploy Dapr to AKS
echo "⚡ Installing Dapr..."
kubectl apply -f https://raw.githubusercontent.com/dapr/dapr/v1.11.0/deployments/charts/dapr_latest_version/charts/dapr-crds/crds/all.yaml
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update
helm install dapr dapr/dapr --namespace dapr-system --create-namespace --wait

# Deploy Azure managed services (instructions)
echo "☁️ Preparing for Azure managed services..."
echo "Please provision these Azure services manually or via ARM templates:"
echo "- Azure Event Hubs (for Kafka replacement)"
echo "- Azure Database for PostgreSQL (for database replacement)"
echo "- Configure the connection strings in your application"

# Deploy LearnFlow application
echo "🚢 Deploying LearnFlow application to AKS..."
kubectl apply -f ../../../learnflow-app/k8s/

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=triage-agent -n default --timeout=300s
kubectl wait --for=condition=ready pod -l app=concepts-agent -n default --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend -n default --timeout=300s

# Get external IP
echo "🌐 Getting external IP address..."
FRONTEND_IP=""
while [ -z "$FRONTEND_IP" ]; do
    FRONTEND_IP=$(kubectl get svc frontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
    if [ -z "$FRONTEND_IP" ]; then
        echo "Waiting for external IP assignment..."
        sleep 10
    fi
done

echo "✅ LearnFlow deployed successfully to Azure!"
echo "Frontend URL: http://$FRONTEND_IP"
echo ""
echo "📝 Next steps:"
echo "1. Configure Azure Event Hubs as Kafka replacement"
echo "2. Configure Azure Database for PostgreSQL"
echo "3. Update application configuration with cloud service endpoints"
echo "4. Set up Azure Monitor for logging and metrics"

# Show deployment status
echo ""
echo "📋 Current deployment status:"
kubectl get pods
kubectl get services