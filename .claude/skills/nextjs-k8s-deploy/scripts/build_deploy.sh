#!/bin/bash

# Next.js Kubernetes Deployment Script
# This script builds a Next.js application and deploys it to Kubernetes

set -e  # Exit on any error

if [ $# -lt 2 ]; then
    echo "Usage: $0 <app_name> <namespace>"
    echo "Example: $0 learnflow-frontend production"
    exit 1
fi

APP_NAME=$1
NAMESPACE=$2

echo "🚀 Building and deploying Next.js application: $APP_NAME to namespace: $NAMESPACE"

# Create namespace if it doesn't exist
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Check if we're in a Next.js project directory
if [ ! -f "package.json" ] || ! grep -q "next" package.json; then
    echo "⚠️  No Next.js project found in current directory. Creating a new one..."

    # Create a basic Next.js project structure for LearnFlow
    if [ ! -d "pages" ] && [ ! -d "src" ]; then
        echo "Creating basic LearnFlow frontend structure..."

        # Create basic files
        mkdir -p pages/api pages/_app public
        touch pages/index.js

        cat > package.json << EOF
{
  "name": "$APP_NAME",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18",
    "react-dom": "^18",
    "@monaco-editor/react": "^4.6.0",
    "better-auth": "^0.1.0"
  },
  "devDependencies": {
    "eslint": "^8",
    "eslint-config-next": "14.0.0"
  }
}
EOF

        cat > pages/index.js << EOF
export default function Home() {
  return (
    <div className="container">
      <h1>Welcome to LearnFlow</h1>
      <p>Your AI-powered Python learning platform</p>
    </div>
  )
}
EOF

        cat > pages/_app.js << EOF
export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />
}
EOF
    fi
fi

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building Next.js application..."
npm run build

# Create optimized Dockerfile if it doesn't exist
if [ ! -f "Dockerfile" ]; then
    echo "📝 Creating optimized Dockerfile..."

    cat > Dockerfile << 'EOF'
# Multi-stage build for optimized image
FROM node:18-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Builder stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Production stage
FROM node:18-alpine AS runner
WORKDIR /app

# Copy production dependencies
COPY --from=base /app/node_modules ./node_modules
# Copy built application
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
ENV PORT=3000
ENV NEXT_TELEMETRY_DISABLED=1

CMD ["node", "server.js"]
EOF
fi

# Build Docker image
IMAGE_TAG="localhost/$APP_NAME:$(date +%s)"
echo "🐳 Building Docker image: $IMAGE_TAG"
docker build -t "$IMAGE_TAG" .

echo "🔄 Deploying to Kubernetes..."

# Create Kubernetes deployment YAML
cat > nextjs-deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $APP_NAME
  namespace: $NAMESPACE
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $APP_NAME
  template:
    metadata:
      labels:
        app: $APP_NAME
    spec:
      containers:
      - name: nextjs
        image: $IMAGE_TAG
        ports:
        - containerPort: 3000
        env:
        - name: PORT
          value: "3000"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: $APP_NAME-service
  namespace: $NAMESPACE
spec:
  selector:
    app: $APP_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: ClusterIP
EOF

# Apply the Kubernetes manifests
kubectl apply -f nextjs-deployment.yaml

# Clean up
rm nextjs-deployment.yaml

echo "✅ Next.js application '$APP_NAME' deployed to namespace '$NAMESPACE'"
echo ""
echo "📋 Access Information:"
echo "  Service: $APP_NAME-service in namespace $NAMESPACE"
echo "  Port: 80 (for internal cluster access)"
echo ""
echo "💡 To access externally, create an ingress or use port forwarding:"
echo "   kubectl port-forward -n $NAMESPACE svc/$APP_NAME-service 3000:80"