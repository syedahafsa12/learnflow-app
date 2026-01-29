#!/usr/bin/env python3
"""
Kafka Topic Creation Script
This script creates Kafka topics in the Kubernetes-deployed Kafka cluster.
"""

import subprocess
import sys
import argparse

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

def get_kafka_pod():
    """Get the name of the Kafka pod."""
    stdout, stderr, code = run_command("kubectl get pods -n kafka -l app.kubernetes.io/name=kafka -o jsonpath='{.items[0].metadata.name}'")

    if code != 0 or not stdout:
        print(f"✗ Could not find Kafka pod: {stderr}")
        return None

    return stdout.strip().strip("'")

def create_topic(topic_name, partitions=1, replication_factor=1):
    """Create a single Kafka topic."""
    kafka_pod = get_kafka_pod()
    if not kafka_pod:
        return False

    print(f"[*] Creating topic '{topic_name}'...")

    cmd = f"kubectl exec -n kafka {kafka_pod} -- kafka-topics.sh --create --topic {topic_name} --bootstrap-server localhost:9092 --partitions {partitions} --replication-factor {replication_factor}"

    stdout, stderr, code = run_command(cmd)

    if code == 0 or "Created topic" in stdout or "already exists" in stdout:
        print(f"  [+] Topic '{topic_name}' created successfully or already exists")
        return True
    else:
        print(f"  [-] Failed to create topic '{topic_name}': {stderr}")
        return False

def list_topics():
    """List all Kafka topics."""
    kafka_pod = get_kafka_pod()
    if not kafka_pod:
        return False

    print("[i] Current topics in Kafka:")

    cmd = f"kubectl exec -n kafka {kafka_pod} -- kafka-topics.sh --list --bootstrap-server localhost:9092"

    stdout, stderr, code = run_command(cmd)

    if code == 0:
        topics = stdout.strip().split('\n') if stdout.strip() else []
        for topic in topics:
            print(f"  - {topic}")
        return True
    else:
        print(f"  [-] Failed to list topics: {stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Create Kafka topics in Kubernetes")
    parser.add_argument('topics', nargs='+', help='Topic names to create')
    parser.add_argument('--partitions', type=int, default=1, help='Number of partitions per topic (default: 1)')
    parser.add_argument('--replication-factor', type=int, default=1, help='Replication factor per topic (default: 1)')
    parser.add_argument('--list', action='store_true', help='List existing topics')

    args = parser.parse_args()

    if args.list:
        list_topics()
        return

    print(f"[*] Creating {len(args.topics)} Kafka topic(s)...")

    success_count = 0
    for topic in args.topics:
        if create_topic(topic, args.partitions, args.replication_factor):
            success_count += 1

    print(f"\n[+] Summary: {success_count}/{len(args.topics)} topics created successfully")

    # List topics after creation
    print("\n[i] Updated topic list:")
    list_topics()

    if success_count == len(args.topics):
        print("\n[+] All topics created successfully!")
        return 0
    else:
        print(f"\n⚠️  Some topics failed to create ({success_count}/{len(args.topics)} succeeded)")
        return 1

if __name__ == "__main__":
    sys.exit(main())