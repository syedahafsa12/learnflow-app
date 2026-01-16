---
name: kafka-k8s-setup
description: Deploy Apache Kafka on Kubernetes with verification and topic management
---

# Kafka Kubernetes Setup

## When to Use
- User asks to deploy Kafka on Kubernetes
- Setting up event-driven microservices architecture
- Creating message queues for asynchronous processing
- Need for pub/sub messaging system

## Instructions
1. Deploy Kafka: `./scripts/deploy_kafka.sh`
2. Verify status: `python scripts/verify_kafka.py`
3. Create topics if needed: `python scripts/create_topics.py <topic_names>`
4. Confirm all pods are Running before proceeding

## Prerequisites
- Kubernetes cluster (Minikube, Kind, or cloud provider)
- Helm 3.x installed
- kubectl configured to access cluster

## Expected Components
- ZooKeeper (for Kafka coordination)
- Kafka brokers
- Kafka Manager/UI (optional)

## Validation
- [ ] All Kafka pods in Running state
- [ ] Kafka service accessible
- [ ] Can create and list topics successfully
- [ ] ZooKeeper pods Running

See [REFERENCE.md](./REFERENCE.md) for advanced configuration options.