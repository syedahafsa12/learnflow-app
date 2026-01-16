# Next.js Kubernetes Deployment - Reference Documentation

## Overview
This skill deploys Next.js applications to Kubernetes with optimized Docker images and production-ready configurations. It's designed for the LearnFlow frontend but can be used for any Next.js application.

## Architecture
The deployment includes:
- Next.js application container with optimized multi-stage build
- Kubernetes Deployment with rolling updates
- Service for network access
- Ingress for external access (optional)

## Docker Image Optimization

### Multi-Stage Build
The Dockerfile uses a three-stage build process:
1. **Base**: Install production dependencies only
2. **Builder**: Build the Next.js application
3. **Runner**: Create minimal production image with only required files

### Security Features
- Non-root user (UID 1001) for running the application
- ReadOnlyRootFilesystem disabled (required for Next.js runtime)
- Drop all capabilities
- No privilege escalation allowed

### Performance Optimizations
- Standalone output mode for faster startup
- Production-only dependencies
- Minimal base image (Alpine Linux)
- Proper resource limits and requests

## Kubernetes Configuration

### Deployment Strategy
- RollingUpdate strategy for zero-downtime deployments
- MaxSurge: 1 (allow 1 extra pod during update)
- MaxUnavailable: 0 (maintain full capacity)

### Resource Configuration
Default resource requests and limits:
- CPU Request: 100m
- CPU Limit: 500m
- Memory Request: 256Mi
- Memory Limit: 512Mi

### Health Checks
- Liveness probe: Check if app is running (after 30s initial delay)
- Readiness probe: Check if app is ready to serve traffic (after 5s initial delay)

## Environment Variables

### Required Variables
- `PORT`: Port number for the application (default: 3000)
- `NODE_ENV`: Environment mode (production/development)
- `NEXT_TELEMETRY_DISABLED`: Disable Next.js telemetry (recommended for production)

### Optional Variables
- `NEXT_PUBLIC_*`: Public environment variables accessible in browser
- `DATABASE_URL`: Database connection string
- `AUTH_SECRET`: Authentication secret for NextAuth.js

## LearnFlow Frontend Specifics

### Monaco Editor Integration
The Dockerfile and deployment are optimized for Monaco Editor:
- Proper CORS configuration
- Adequate memory allocation for editor worker processes
- Correct MIME type handling for WASM files

### TailwindCSS Optimization
- Purged for production builds
- JIT compiler for faster builds
- Responsive design support

## Template Variables
The Kubernetes templates use these variables:
- `{{APP_NAME}}`: Name of the application
- `{{NAMESPACE}}`: Kubernetes namespace
- `{{IMAGE_NAME}}`: Docker image name and tag
- `{{REPLICAS}}`: Number of pod replicas (default: 1)
- `{{MEMORY_REQUEST}}`: Memory request (default: 256Mi)
- `{{MEMORY_LIMIT}}`: Memory limit (default: 512Mi)
- `{{CPU_REQUEST}}`: CPU request (default: 100m)
- `{{CPU_LIMIT}}`: CPU limit (default: 500m)
- `{{SERVICE_TYPE}}`: Service type (ClusterIP, NodePort, LoadBalancer)
- `{{HOSTNAME}}`: Hostname for ingress (optional)

## Ingress Configuration
The default ingress configuration:
- Rewrites paths to root
- HTTP routing only (TLS termination typically handled by load balancer)
- Supports custom hostnames

## Monitoring and Logging

### Built-in Monitoring
- Health check endpoint: `/health`
- Metrics available through Next.js
- Container logs accessible via kubectl

### Recommended Monitoring
- Resource utilization (CPU, memory)
- Response times
- Error rates
- Traffic patterns

## Scaling Recommendations

### Vertical Scaling
Increase resources for:
- Heavy computations
- Large bundles
- Multiple concurrent users

### Horizontal Scaling
Increase replicas for:
- High traffic
- Availability requirements
- Load distribution

## Security Considerations
- Use secrets for sensitive configuration
- Enable RBAC for service accounts
- Configure network policies
- Regular security scanning of images
- HTTPS enforcement

## Troubleshooting

### Common Issues
1. **Application not starting**: Check logs for build errors
2. **High memory usage**: Increase memory limits
3. **Slow builds**: Optimize dependencies
4. **Missing environment variables**: Verify deployment configuration

### Diagnostic Commands
```bash
# Check deployment status
kubectl get deployment <app-name> -n <namespace>

# View pod logs
kubectl logs -n <namespace> deployment/<app-name> -f

# Describe deployment for events
kubectl describe deployment <app-name> -n <namespace>

# Check service endpoints
kubectl get endpoints <app-name>-service -n <namespace>
```

## Performance Tuning
- Adjust resource limits based on actual usage
- Enable compression for static assets
- Optimize image sizes
- Use CDN for static assets
- Implement caching strategies

## Integration with LearnFlow
For the LearnFlow platform, this skill provides:
- Responsive frontend for students and teachers
- Monaco editor integration for code writing
- Real-time updates from backend services
- Authentication integration
- Mobile-friendly design