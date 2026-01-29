#!/bin/bash

# Next.js Kubernetes Deployment Script
# Builds and deploys a Next.js application to Kubernetes

set -e  # Exit on any error

if [ $# -eq 0 ]; then
    echo "Usage: $0 <app_name> [image_tag]"
    exit 1
fi

APP_NAME=$1
IMAGE_TAG=${2:-"latest"}
IMAGE_NAME="${APP_NAME}:${IMAGE_TAG}"

echo "Building and deploying Next.js application: $APP_NAME"

# Create app directory if it doesn't exist
if [ ! -d "$APP_NAME" ]; then
    echo "Creating Next.js application: $APP_NAME"
    
    # Create Next.js app with TypeScript, Tailwind CSS, and App Router
    npx create-next-app@latest "$APP_NAME" --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
    
    # Navigate to app directory
    cd "$APP_NAME"
    
    # Install additional dependencies for LearnFlow frontend
    npm install @monaco-editor/react monaco-editor
    npm install better-auth zustand react-hot-toast
    npm install -D @types/better-auth
    
    # Add Monaco Editor configuration
    cat > public/monaco-editor/workbench.html << 'MONACO_EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monaco Editor Workbench</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
MONACO_EOF

    # Update package.json to add build configuration
    if command -v jq >/dev/null 2>&1; then
        jq '.scripts += {"build-static": "next build && next export"}' package.json > tmp_package.json && mv tmp_package.json package.json
    else
        echo "jq not found, skipping package.json update"
    fi
    
    cd ..
else
    echo "Using existing application: $APP_NAME"
    cd "$APP_NAME"
fi

# Create Dockerfile for Next.js app
cat > Dockerfile << DOCKERFILE_EOF
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else npm ci; \
  fi


# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the build.
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000

# server.js is created by next build from the standalone output
# https://nextjs.org/docs/pages/api-reference/next-config-js/output
CMD ["node", "server.js"]
DOCKERFILE_EOF

# Create .dockerignore
cat > .dockerignore << DOCKERIGNORE_EOF
Dockerfile
.dockerignore
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.vscode
DOCKERIGNORE_EOF

# Build Docker image
echo "Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" .

# Tag for minikube
eval $(minikube docker-env)
docker tag "$IMAGE_NAME" "$IMAGE_NAME"

cd ..

# Create Kubernetes manifests
MANIFEST_DIR="./k8s-manifests-$APP_NAME"
mkdir -p "$MANIFEST_DIR"

# Create Deployment
cat > "$MANIFEST_DIR/deployment.yaml" << DEPLOYMENT_EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}-deployment
  labels:
    app: $APP_NAME
spec:
  replicas: 2
  selector:
    matchLabels:
      app: $APP_NAME
  template:
    metadata:
      labels:
        app: $APP_NAME
    spec:
      containers:
      - name: $APP_NAME
        image: $IMAGE_NAME
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: PORT
          value: "3000"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
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
DEPLOYMENT_EOF

# Create Service
cat > "$MANIFEST_DIR/service.yaml" << SERVICE_EOF
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}-service
  labels:
    app: $APP_NAME
spec:
  selector:
    app: $APP_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
SERVICE_EOF

# Create Ingress (optional)
cat > "$MANIFEST_DIR/ingress.yaml" << INGRESS_EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: $APP_NAME.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ${APP_NAME}-service
            port:
              number: 80
INGRESS_EOF

# Apply the manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f "$MANIFEST_DIR/"

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/${APP_NAME}-deployment --timeout=300s

# Get the service information
echo "Getting service information..."
kubectl get svc ${APP_NAME}-service

echo "✓ Next.js application $APP_NAME deployed successfully to Kubernetes!"
echo "Deployment name: ${APP_NAME}-deployment"
echo "Service name: ${APP_NAME}-service"
echo "Access via minikube: minikube service ${APP_NAME}-service --url"
