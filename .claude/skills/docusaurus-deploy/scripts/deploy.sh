#!/bin/bash

# Docusaurus Documentation Deployment Script
# This script creates and deploys a Docusaurus site to Kubernetes

set -e  # Exit on any error

if [ $# -lt 2 ]; then
    echo "Usage: $0 <site_name> <namespace>"
    echo "Example: $0 learnflow-docs production"
    exit 1
fi

SITE_NAME=$1
NAMESPACE=$2

echo "🚀 Creating and deploying Docusaurus site: $SITE_NAME to namespace: $NAMESPACE"

# Create namespace if it doesn't exist
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Check if we're in a Docusaurus project directory
if [ ! -f "docusaurus.config.js" ] && [ ! -f "docusaurus.config.ts" ] && [ ! -f "package.json" ] || ! grep -q "docusaurus" package.json; then
    echo "📝 Initializing new Docusaurus site..."

    # Install Docusaurus globally if not available
    npm install -g @docusaurus/core@latest

    # Create a new Docusaurus site
    npx create-docusaurus@latest "$SITE_NAME" classic --typescript

    # Navigate to the new site directory
    cd "$SITE_NAME"
fi

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building Docusaurus site..."
npm run build

# Create optimized Dockerfile for Docusaurus
cat > Dockerfile << 'EOF'
# Multi-stage build for optimized Docusaurus image
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine AS production
WORKDIR /usr/share/nginx/html
COPY --from=builder /app/build ./
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF

# Create optimized nginx configuration
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Gzip compression for static assets
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json
        application/x-javascript;

    server {
        listen 80;
        root /usr/share/nginx/html;
        index index.html;

        # Handle client-side routing for SPAs
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Set headers for static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
    }
}
EOF

# Build Docker image
IMAGE_TAG="localhost/$SITE_NAME-docs:$(date +%s)"
echo "🐳 Building Docker image: $IMAGE_TAG"
docker build -t "$IMAGE_TAG" .

echo "🔄 Deploying to Kubernetes..."

# Create Kubernetes deployment YAML
cat > docusaurus-deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $SITE_NAME
  namespace: $NAMESPACE
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $SITE_NAME
  template:
    metadata:
      labels:
        app: $SITE_NAME
    spec:
      containers:
      - name: docusaurus
        image: $IMAGE_TAG
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "50m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: $SITE_NAME-service
  namespace: $NAMESPACE
spec:
  selector:
    app: $SITE_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
EOF

# Apply the Kubernetes manifests
kubectl apply -f docusaurus-deployment.yaml

# Clean up
rm docusaurus-deployment.yaml

echo "✅ Docusaurus site '$SITE_NAME' deployed to namespace '$NAMESPACE'"
echo ""
echo "📋 Access Information:"
echo "  Service: $SITE_NAME-service in namespace $NAMESPACE"
echo "  Port: 80 (for internal cluster access)"
echo ""
echo "💡 To access externally, create an ingress or use port forwarding:"
echo "   kubectl port-forward -n $NAMESPACE svc/$SITE_NAME-service 8080:80"