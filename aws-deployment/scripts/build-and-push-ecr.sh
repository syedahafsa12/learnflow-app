#!/bin/bash
set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

echo "[*] Building and pushing LearnFlow images to ECR..."
echo "    Region: $AWS_REGION"
echo "    Account: $AWS_ACCOUNT_ID"
echo "    Registry: $ECR_REGISTRY"

# Login to ECR
echo "[*] Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Function to create ECR repository if it doesn't exist
create_ecr_repo() {
    local repo_name=$1
    echo "[*] Checking ECR repository: $repo_name"

    if ! aws ecr describe-repositories --repository-names $repo_name --region $AWS_REGION >/dev/null 2>&1; then
        echo "    Creating repository: $repo_name"
        aws ecr create-repository \
            --repository-name $repo_name \
            --region $AWS_REGION \
            --image-scanning-configuration scanOnPush=true \
            --encryption-configuration encryptionType=AES256 >/dev/null
    else
        echo "    Repository exists: $repo_name"
    fi
}

# Function to build, tag, and push image
build_and_push() {
    local service_name=$1
    local service_dir=$2
    local repo_name="learnflow/${service_name}"

    echo "[*] Building $service_name..."

    # Create ECR repository
    create_ecr_repo $repo_name

    # Build image
    docker build -t $service_name:latest $service_dir

    # Tag for ECR
    docker tag $service_name:latest ${ECR_REGISTRY}/${repo_name}:latest
    docker tag $service_name:latest ${ECR_REGISTRY}/${repo_name}:$(git rev-parse --short HEAD)

    # Push to ECR
    echo "    Pushing to ECR..."
    docker push ${ECR_REGISTRY}/${repo_name}:latest
    docker push ${ECR_REGISTRY}/${repo_name}:$(git rev-parse --short HEAD)

    echo "    [OK] $service_name pushed successfully"
}

# Build and push all microservices
echo ""
echo "[*] Building and pushing backend microservices..."
build_and_push "triage-agent" "./backend/triage-agent"
build_and_push "concepts-agent" "./backend/concepts-agent"
build_and_push "code-review-agent" "./backend/code-review-agent"
build_and_push "debug-agent" "./backend/debug-agent"
build_and_push "exercise-agent" "./backend/exercise-agent"
build_and_push "progress-agent" "./backend/progress-agent"

# Build and push frontend (if exists)
if [ -d "./frontend" ]; then
    echo ""
    echo "[*] Building and pushing frontend..."
    build_and_push "learnflow-frontend" "./frontend"
fi

echo ""
echo "[OK] All images built and pushed to ECR successfully!"
echo ""
echo "Image URIs:"
for service in triage-agent concepts-agent code-review-agent debug-agent exercise-agent progress-agent; do
    echo "  ${ECR_REGISTRY}/learnflow/${service}:latest"
done

echo ""
echo "Next steps:"
echo "1. Update Kubernetes manifests with ECR image URIs"
echo "2. Deploy to EKS: kubectl apply -f aws-deployment/manifests/"
