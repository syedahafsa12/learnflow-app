---
name: kafka-k8s-setup
description: Deploy Apache Kafka on Kubernetes
---

# Kafka Kubernetes Setup

## When to Use
- User asks to deploy Kafka
- Setting up event-driven microservices
- Need message queuing capabilities

## Instructions
1. Run deployment: `bash scripts/deploy.sh`
2. Verify status: `python scripts/verify.py`
3. Create topics: `bash scripts/create_topics.sh`
4. Confirm all pods Running before proceeding.

## Validation
- [ ] All pods in Running state
- [ ] Can create test topic
- [ ] Kafka brokers are accessible

See [REFERENCE.md](./REFERENCE.md) for configuration options.
