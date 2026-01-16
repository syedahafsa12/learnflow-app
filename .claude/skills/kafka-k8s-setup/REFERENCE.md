# Kafka Kubernetes Setup - Reference Documentation

## Overview
This skill deploys Apache Kafka on Kubernetes using the Bitnami Helm chart. It provides a complete event streaming platform for building real-time data pipelines and streaming applications.

## Architecture
The deployment includes:
- Kafka Brokers: Handle message publishing and consumption
- ZooKeeper: Coordination service for Kafka cluster management
- Services: Network access points for clients

## Configuration Options

### Helm Chart Values
The deployment uses the following configurable parameters:

#### Kafka Configuration
- `replicaCount`: Number of Kafka broker replicas (default: 1)
- `auth.clientProtocol`: Client authentication protocol
- `service.type`: Service type (ClusterIP, NodePort, LoadBalancer)
- `resources.limits.memory`: Memory limits for Kafka pods
- `persistence.enabled`: Enable/disable persistent storage

#### ZooKeeper Configuration
- `zookeeper.replicaCount`: Number of ZooKeeper replicas
- `zookeeper.persistence.enabled`: Enable/disable ZooKeeper persistence

### Custom Values File
You can create a custom values file for advanced configuration:

```yaml
# kafka-values.yaml
kafka:
  replicaCount: 3
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi
  persistence:
    enabled: true
    size: 10Gi

zookeeper:
  replicaCount: 3
  persistence:
    enabled: true
    size: 8Gi
```

Then deploy with: `helm install kafka -f kafka-values.yaml bitnami/kafka --namespace kafka`

## Topic Management

### Creating Topics
Topics can be created with specific configurations:
- Partitions: Determine parallelism for consumers
- Replication Factor: Determine fault tolerance
- Retention Policy: Configure how long messages are kept

### Topic Naming Convention
Recommended naming convention for LearnFlow topics:
- `learning.*` - Student learning events
- `code.*` - Code execution events
- `exercise.*` - Exercise completion events
- `struggle.*` - Struggle detection events

## Networking

### Internal Access
Within the Kubernetes cluster:
- Bootstrap server: `kafka.kafka.svc.cluster.local:9092`

### External Access
For external access, use port forwarding:
```bash
kubectl port-forward -n kafka svc/kafka 9092:9092
```

Or configure a LoadBalancer service type.

## Security Considerations
- Enable authentication for production deployments
- Use TLS encryption for data in transit
- Limit resource usage to prevent DoS
- Restrict network access with NetworkPolicies

## Monitoring and Logging
- Monitor pod health with `kubectl get pods`
- Check logs with `kubectl logs -n kafka <pod-name>`
- Use Prometheus and Grafana for metrics

## Troubleshooting

### Common Issues
1. **Pods stuck in Pending**: Check resource availability
2. **Connection timeouts**: Verify service networking
3. **Insufficient storage**: Ensure PersistentVolumes are available
4. **ZooKeeper issues**: Check ZooKeeper ensemble health

### Diagnostic Commands
```bash
# Check all resources in kafka namespace
kubectl get all -n kafka

# Describe Kafka pods for events
kubectl describe pod -l app.kubernetes.io/name=kafka -n kafka

# Check ZooKeeper status
kubectl exec -n kafka <zk-pod> -- zkCli.sh -server localhost:2181 ls /

# List topics
kubectl exec -n kafka <kafka-pod> -- kafka-topics.sh --list --bootstrap-server localhost:9092
```

## Scaling
- Scale brokers by changing `replicaCount`
- Adjust partitions per topic based on throughput needs
- Monitor resource usage and adjust limits accordingly

## Cleanup
To remove the Kafka deployment:
```bash
helm uninstall kafka -n kafka
kubectl delete namespace kafka
```

## Integration with LearnFlow
For the LearnFlow platform, Kafka topics should be created for:
- Student activity tracking
- Code execution results
- Exercise completion events
- Struggle detection notifications
- Progress updates