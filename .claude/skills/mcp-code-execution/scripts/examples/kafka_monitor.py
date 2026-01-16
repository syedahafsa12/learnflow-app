#!/usr/bin/env python3
"""
Example: Kafka Monitoring using MCP Code Execution Pattern
This script demonstrates how to efficiently monitor Kafka
while minimizing token usage in the agent context.
"""

import subprocess
import sys
import json

def run_command(cmd):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip(), result.stderr.strip(), 0
    except subprocess.CalledProcessError as e:
        return e.stdout.strip(), e.stderr.strip(), e.returncode

def get_kafka_pod(namespace="kafka"):
    """Get the name of the Kafka pod."""
    stdout, stderr, code = run_command(f"kubectl get pods -n {namespace} -l app.kubernetes.io/name=kafka -o jsonpath='{{.items[0].metadata.name}}'")

    if code != 0 or not stdout:
        return None

    return stdout.strip().strip("'")

def check_kafka_health():
    """Check Kafka health with minimal output."""

    kafka_pod = get_kafka_pod()
    if not kafka_pod:
        return "❌ Cannot find Kafka pod", False

    # Check if Kafka is responsive by listing topics
    cmd = f"kubectl exec -n kafka {kafka_pod} -- kafka-topics.sh --list --bootstrap-server localhost:9092"
    stdout, stderr, code = run_command(cmd)

    if code != 0:
        return f"❌ Kafka not responding: {stderr[:100]}", False

    topics = [t.strip() for t in stdout.split('\n') if t.strip()]

    # Check if there are any topics
    if not topics:
        return "⚠️  Kafka running but no topics exist", True

    # Get details about one topic to verify functionality
    first_topic = topics[0]
    cmd = f"kubectl exec -n kafka {kafka_pod} -- kafka-topics.sh --describe --topic {first_topic} --bootstrap-server localhost:9092"
    stdout, stderr, code = run_command(cmd)

    if code != 0:
        return f"⚠️  Kafka running but topic {first_topic} not accessible: {stderr[:100]}", False

    # Count partitions to verify topic health
    partition_count = stdout.count("Partition")

    return f"✅ Kafka healthy: {len(topics)} topics, first topic '{first_topic}' has {partition_count} partitions", True

def main():
    """Main function to check Kafka health."""
    print("Checking Kafka health...")

    status_message, is_healthy = check_kafka_health()
    print(status_message)

    # Return exit code based on health status
    sys.exit(0 if is_healthy else 1)

if __name__ == "__main__":
    main()