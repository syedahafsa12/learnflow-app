#!/bin/bash
# Build and deploy Docusaurus site to Kubernetes

SITE_NAME=${1:-"learnflow-docs"}

echo "Building Docusaurus site: $SITE_NAME"

# Navigate to the site directory
cd /tmp || exit 1
if [ ! -d "$SITE_NAME" ]; then
    echo "Site directory $SITE_NAME does not exist. Creating new Docusaurus site..."
    npx create-docusaurus@latest "$SITE_NAME" classic --typescript
    cd "$SITE_NAME"
else
    cd "$SITE_NAME"
fi

# Build the site
npm run build

# Create Dockerfile for the built site
cat > Dockerfile << 'EOF'
FROM nginx:alpine
COPY ./build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF

# Build Docker image
IMAGE_NAME="docusaurus-$SITE_NAME:$(date +%s)"
docker build -t "$IMAGE_NAME" .

# Tag and push to local registry (for minikube)
eval $(minikube docker-env)
docker tag "$IMAGE_NAME" "docusaurus-$SITE_NAME:latest"
docker push "docusaurus-$SITE_NAME:latest"

# Create Kubernetes deployment
cat > deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $SITE_NAME-deployment
  namespace: default
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
        image: docusaurus-$SITE_NAME:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: $SITE_NAME-service
spec:
  selector:
    app: $SITE_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
EOF

# Apply the deployment
kubectl apply -f deployment.yaml

echo "✓ Docusaurus site $SITE_NAME built and deployed to Kubernetes"