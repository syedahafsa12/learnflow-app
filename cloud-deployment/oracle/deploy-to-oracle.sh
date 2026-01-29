#!/bin/bash

# Deploy LearnFlow to Oracle Container Engine for Kubernetes (OKE)
# This script automates the deployment process to Oracle Cloud

set -e  # Exit on any error

echo "🚀 Deploying LearnFlow to Oracle Container Engine for Kubernetes..."

# Check if OCI CLI is installed
if ! command -v oci &> /dev/null; then
    echo "❌ Oracle Cloud Infrastructure CLI is not installed. Please install it first."
    echo "Installation: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install it first."
    exit 1
fi

# Login to Oracle Cloud (you may need to authenticate)
echo "🔐 Authenticating with Oracle Cloud..."
echo "Note: Ensure you have configured OCI CLI with 'oci setup config'"
oci setup repair-file-permissions --file ~/.oci/config
oci setup repair-file-permissions --file ~/.oci/oci_api_key.pem

# Set up configuration
echo "💳 Setting Oracle Cloud configuration..."
read -p "Enter your Oracle Cloud Tenancy OCID: " TENANCY_OCID
read -p "Enter your Oracle Cloud User OCID: " USER_OCID
read -p "Enter your Oracle Cloud Region (e.g., us-ashburn-1): " REGION

# Configure OCI
oci setup config --file ~/.oci/config << EOF
$TENANCY_OCID
$USER_OCID
$REGION
EOF

# Create VCN and OKE cluster
echo "🏗️ Creating VCN and OKE cluster..."
read -p "Enter compartment OCID: " COMPARTMENT_OCID
read -p "Enter OKE cluster name (default: learnflow-oke): " OKE_CLUSTER_NAME
OKE_CLUSTER_NAME=${OKE_CLUSTER_NAME:-"learnflow-oke"}

# Create VCN first
echo "🌐 Creating Virtual Cloud Network..."
VCN_NAME="learnflow-vcn"
oci network vcn create --compartment-id $COMPARTMENT_OCID --display-name $VCN_NAME --cidr-block "10.0.0.0/16"

# Get VCN ID
VCN_ID=$(oci network vcn list --compartment-id $COMPARTMENT_OCID --display-name $VCN_NAME --query "data[0].id" --raw-output)

# Create subnets
echo "🏠 Creating subnets..."
PUBLIC_SUBNET_1=$(oci network subnet create --compartment-id $COMPARTMENT_OCID --availability-domain-1 --vcn-id $VCN_ID --display-name "learnflow-public-subnet-1" --cidr-block "10.0.1.0/24" --query "data.id" --raw-output)
PRIVATE_SUBNET_1=$(oci network subnet create --compartment-id $COMPARTMENT_OCID --availability-domain-1 --vcn-id $VCN_ID --display-name "learnflow-private-subnet-1" --cidr-block "10.0.2.0/24" --query "data.id" --raw-output)

# Create OKE cluster
echo "🐳 Creating OKE cluster..."
oci ce cluster create --name $OKE_CLUSTER_NAME --kubernetes-version "v1.26.2" --compartment-id $COMPARTMENT_OCID --vcn-id $VCN_ID --service-lb-subnet-ids "[\"$PUBLIC_SUBNET_1\"]" --worker-node-subnet-ids "[\"$PRIVATE_SUBNET_1\"]"

# Wait for cluster to be active
echo "⏳ Waiting for cluster to be active..."
CLUSTER_ID=$(oci ce cluster list --compartment-id $COMPARTMENT_OCID --name $OKE_CLUSTER_NAME --query "data[0].id" --raw-output)
while [ "$(oci ce cluster get --cluster-id $CLUSTER_ID --query "data.lifecycle-state" --raw-output)" != "ACTIVE" ]; do
    echo "Waiting for cluster to be ACTIVE..."
    sleep 30
done

# Get OKE credentials
echo "🔑 Getting OKE credentials..."
oci ce cluster create-kubeconfig --cluster-id $CLUSTER_ID --file $HOME/.kube/config --region $REGION

# Deploy Dapr to OKE
echo "⚡ Installing Dapr..."
kubectl apply -f https://raw.githubusercontent.com/dapr/dapr/v1.11.0/deployments/charts/dapr_latest_version/charts/dapr-crds/crds/all.yaml
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update
helm install dapr dapr/dapr --namespace dapr-system --create-namespace --wait

# Deploy Oracle managed services (instructions)
echo "☁️ Preparing for Oracle Cloud managed services..."
echo "Please provision these Oracle Cloud services manually or via Terraform:"
echo "- Oracle Streaming Service (for Kafka replacement)"
echo "- Oracle Autonomous Transaction Processing Database (for database replacement)"
echo "- Configure the connection strings in your application"

# Deploy LearnFlow application
echo "🚢 Deploying LearnFlow application to OKE..."
kubectl apply -f ../../../learnflow-app/k8s/

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=triage-agent -n default --timeout=300s
kubectl wait --for=condition=ready pod -l app=concepts-agent -n default --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend -n default --timeout=300s

# Set up Load Balancer
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

echo "✅ LearnFlow deployed successfully to Oracle Cloud!"
echo "Frontend URL: http://$FRONTEND_IP"
echo ""
echo "📝 Next steps:"
echo "1. Configure Oracle Streaming Service as Kafka replacement"
echo "2. Configure Oracle Autonomous Database"
echo "3. Update application configuration with cloud service endpoints"
echo "4. Set up OCI Monitoring for metrics and logging"

# Show deployment status
echo ""
echo "📋 Current deployment status:"
kubectl get pods
kubectl get services