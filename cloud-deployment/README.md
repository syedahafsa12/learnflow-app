# Cloud Deployment for LearnFlow

This directory contains configurations for deploying LearnFlow to cloud platforms:

- **Azure**: Using Azure Kubernetes Service (AKS)
- **Google Cloud**: Using Google Kubernetes Engine (GKE)
- **Oracle Cloud**: Using Oracle Container Engine for Kubernetes (OKE)

## Deployment Strategy

The LearnFlow application will be deployed using the same Kubernetes manifests that work in Minikube, with cloud-specific configurations for:

- Managed Kafka service (instead of in-cluster)
- Managed PostgreSQL service (instead of in-cluster)
- Cloud load balancers and networking
- Cloud-native monitoring and logging

## Cloud Provider Options

Choose one of the following cloud providers:

### Azure (Recommended)
- AKS for Kubernetes orchestration
- Azure Event Hubs for Kafka-compatible messaging
- Azure Database for PostgreSQL
- Azure Monitor for logging and metrics

### Google Cloud
- GKE for Kubernetes orchestration
- Google Cloud Pub/Sub for messaging
- Google Cloud SQL for PostgreSQL
- Google Cloud Operations Suite for monitoring

### Oracle Cloud
- OKE for Kubernetes orchestration
- Streaming service for messaging
- Autonomous Database for PostgreSQL
- OCI Monitoring for metrics and logging