#!/bin/bash

# Kafka Topic Creation Script
# Creates default topics needed for LearnFlow application

set -e  # Exit on any error

echo "Creating Kafka topics for LearnFlow..."

# Wait for Kafka to be fully ready
sleep 15

# Create topics for LearnFlow application
kubectl exec -n kafka deploy/kafka -- kafka-topics.sh --create --topic learning.progress --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
kubectl exec -n kafka deploy/kafka -- kafka-topics.sh --create --topic code.execution --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
kubectl exec -n kafka deploy/kafka -- kafka-topics.sh --create --topic code.review --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
kubectl exec -n kafka deploy/kafka -- kafka-topics.sh --create --topic learning.struggle --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
kubectl exec -n kafka deploy/kafka -- kafka-topics.sh --create --topic exercise.submission --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092

# List all topics to confirm creation
echo "Created topics:"
kubectl exec -n kafka deploy/kafka -- kafka-topics.sh --list --bootstrap-server localhost:9092

echo "✓ Kafka topics created successfully!"
