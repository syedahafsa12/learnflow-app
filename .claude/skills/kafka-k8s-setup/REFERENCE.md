# Kafka Kubernetes Setup Reference

## Purpose
The Kafka Kubernetes Setup skill deploys and manages Apache Kafka clusters on Kubernetes for event-driven architectures.

## Features
- Automated Kafka and Zookeeper deployment
- Multi-topic creation for LearnFlow application
- Comprehensive verification checks
- Configuration customization

## Usage Patterns
### Basic Deployment
```bash
bash scripts/deploy.sh
```

### Verification
```bash
python scripts/verify.py
```

### Topic Creation
```bash
bash scripts/create_topics.sh
```

## Configuration Options
- Adjust replica counts in deploy.sh
- Modify topic partitions in create_topics.sh
- Change namespace if needed
- Configure persistence settings

## LearnFlow Topics
The skill creates these topics for the LearnFlow application:
- `learning.progress` - Track student progress
- `code.execution` - Handle code execution requests
- `code.review` - Manage code review results
- `learning.struggle` - Detect and handle student struggles
- `exercise.submission` - Process exercise submissions

## Dependencies
- Kubernetes cluster
- Helm 3+
- kubectl
- Sufficient cluster resources (recommended: 4 CPU, 8GB RAM)

## Best Practices
- Monitor cluster resources during deployment
- Verify all pods are running before creating topics
- Adjust partition counts based on expected load
- Use appropriate replication factors for production

## Integration with AI Agents
- Claude Code can deploy Kafka with single command
- Goose can manage topics and verify status
- Provides event streaming backbone for microservices
