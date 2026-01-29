# LearnFlow Documentation

## Overview
LearnFlow is an AI-powered learning platform that helps students learn Python programming concepts through intelligent tutoring, code review, and personalized exercises.

## Architecture

### Backend Services
- **triage-agent**: Routes student queries to specialist agents
- **concepts-agent**: Explains Python concepts with examples
- **code-review-agent**: Analyzes student code for quality
- **debug-agent**: Helps students fix errors
- **exercise-agent**: Generates coding challenges
- **progress-agent**: Tracks student mastery

### Infrastructure
- **Kafka**: Event streaming for microservices communication
- **PostgreSQL**: Data persistence for user data and progress
- **Dapr**: Service mesh for microservices orchestration

### Frontend
- **Next.js Dashboard**: Modern UI with Monaco editor for coding
- **Student View**: Chat interface, code editor, and progress tracking
- **Teacher View**: Class monitoring and struggle alerts

## Event Flow Design
- Student submits code → `code.execution` topic
- Agent reviews → `code.review` topic
- Progress updates → `learning.progress` topic
- Struggles detected → `learning.struggle` topic

## Skills Library
The platform uses a comprehensive skills library for autonomous deployment:

### Infrastructure Skills
- **k8s-foundation**: Basic Kubernetes setup
- **kafka-k8s-setup**: Apache Kafka on Kubernetes
- **postgres-k8s-setup**: PostgreSQL with migrations
- **docusaurus-deploy**: Documentation site deployment

### Application Skills
- **fastapi-dapr-agent**: FastAPI microservices with Dapr
- **nextjs-k8s-deploy**: Next.js application deployment
- **agents-md-gen**: AI agents documentation generator
- **mcp-code-execution**: MCP Code Execution pattern implementation

## Getting Started

### Prerequisites
- Kubernetes cluster (Minikube or cloud provider)
- Dapr installed
- Docker

### Deployment
All services can be deployed autonomously using the skills library:

```bash
# Deploy infrastructure
Deploy Kafka for event-driven architecture
Deploy PostgreSQL with LearnFlow schema

# Deploy backend microservices
Create triage-agent microservice with Dapr
Create concepts-agent microservice
Create code-review-agent microservice
Create debug-agent microservice
Create exercise-agent microservice
Create progress-agent microservice

# Deploy frontend
Deploy Next.js frontend with Monaco editor
```

## Key Features

### AI-Powered Learning
- Intelligent concept explanations
- Real-time code review and feedback
- Personalized exercise generation
- Debugging assistance

### Progress Tracking
- Mastery tracking for concepts
- Struggle detection and alerts
- Performance analytics

### Developer Experience
- Monaco editor integration
- Real-time collaboration
- Version control integration

## Technologies Used

### Backend
- FastAPI for microservices
- Dapr for service mesh
- Python 3.11+

### Frontend
- Next.js 14+ (App Router)
- React with TypeScript
- Monaco Editor for code editing
- TailwindCSS for styling

### Infrastructure
- Kubernetes for orchestration
- Apache Kafka for event streaming
- PostgreSQL for data persistence
- Docker for containerization

## Contributing
The skills library allows AI agents to autonomously extend and enhance the platform with minimal human intervention.

## License
MIT License