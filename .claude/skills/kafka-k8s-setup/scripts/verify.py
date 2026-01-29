#!/usr/bin/env python3
"""
Kafka Verification Script
Verifies that Kafka is properly deployed and accessible
"""

import subprocess
import json
import sys
import time

def check_kafka_pods():
    """Check if Kafka pods are running."""
    try:
        result = subprocess.run([
            "kubectl", "get", "pods", 
            "-n", "kafka", 
            "-l", "app.kubernetes.io/name=kafka",
            "-o", "json"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Error getting Kafka pods: {result.stderr}")
            return False

        pods_data = json.loads(result.stdout)
        pods = pods_data["items"]

        if not pods:
            print("✗ No Kafka pods found")
            return False

        running_count = 0
        total_count = len(pods)

        for pod in pods:
            phase = pod["status"]["phase"]
            if phase == "Running":
                # Check if containers are ready
                container_statuses = pod["status"].get("containerStatuses", [])
                if all(container.get("ready", False) for container in container_statuses):
                    running_count += 1

        if running_count == total_count:
            print(f"✓ All {total_count} Kafka pods are running and ready")
            return True
        else:
            print(f"✗ {running_count}/{total_count} Kafka pods are running and ready")
            return False

    except Exception as e:
        print(f"✗ Error checking Kafka pods: {str(e)}")
        return False

def check_zookeeper_pods():
    """Check if Zookeeper pods are running."""
    try:
        result = subprocess.run([
            "kubectl", "get", "pods", 
            "-n", "kafka", 
            "-l", "app.kubernetes.io/name=zookeeper",
            "-o", "json"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Error getting Zookeeper pods: {result.stderr}")
            return False

        pods_data = json.loads(result.stdout)
        pods = pods_data["items"]

        if not pods:
            print("✗ No Zookeeper pods found")
            return False

        running_count = 0
        total_count = len(pods)

        for pod in pods:
            phase = pod["status"]["phase"]
            if phase == "Running":
                # Check if containers are ready
                container_statuses = pod["status"].get("containerStatuses", [])
                if all(container.get("ready", False) for container in container_statuses):
                    running_count += 1

        if running_count == total_count:
            print(f"✓ All {total_count} Zookeeper pods are running and ready")
            return True
        else:
            print(f"✗ {running_count}/{total_count} Zookeeper pods are running and ready")
            return False

    except Exception as e:
        print(f"✗ Error checking Zookeeper pods: {str(e)}")
        return False

def check_kafka_service():
    """Check if Kafka service is available."""
    try:
        result = subprocess.run([
            "kubectl", "get", "svc", 
            "-n", "kafka", 
            "-l", "app.kubernetes.io/name=kafka"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Error getting Kafka service: {result.stderr}")
            return False

        if "kafka" in result.stdout:
            print("✓ Kafka service is available")
            return True
        else:
            print("✗ Kafka service not found")
            return False

    except Exception as e:
        print(f"✗ Error checking Kafka service: {str(e)}")
        return False

def test_topic_creation():
    """Test if we can create a test topic."""
    try:
        # Wait a bit to ensure Kafka is fully ready
        time.sleep(10)
        
        # Try to create a test topic
        result = subprocess.run([
            "kubectl", "exec",
            "-n", "kafka",
            "deploy/kafka",
            "--",
            "kafka-topics.sh",
            "--create",
            "--topic", "test-topic",
            "--partitions", "1",
            "--replication-factor", "1",
            "--bootstrap-server", "localhost:9092"
        ], capture_output=True, text=True)

        if result.returncode == 0 or "Created topic" in result.stdout or "already exists" in result.stdout:
            print("✓ Successfully created/verified test topic")
            return True
        else:
            print(f"✗ Failed to create test topic: {result.stderr}")
            return False

    except Exception as e:
        print(f"✗ Error testing topic creation: {str(e)}")
        return False

def main():
    print("Verifying Kafka deployment...")

    checks = [
        ("Kafka pods", check_kafka_pods),
        ("Zookeeper pods", check_zookeeper_pods),
        ("Kafka service", check_kafka_service),
        ("Topic creation", test_topic_creation)
    ]

    all_passed = True

    for check_name, check_func in checks:
        print(f"\n{check_name}...")
        if not check_func():
            all_passed = False

    if all_passed:
        print("\n✓ Kafka verification successful! All components are ready.")
        sys.exit(0)
    else:
        print("\n✗ Kafka verification failed! Some components are not ready.")
        sys.exit(1)

if __name__ == "__main__":
    main()
