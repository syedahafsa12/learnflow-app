#!/usr/bin/env python3
"""
Verify FastAPI + Dapr service deployment
"""
import subprocess
import json
import sys
import time

def verify_service(service_name: str, namespace: str = "default"):
    """Verify service is running with Dapr sidecar"""

    # Get pod status
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace, "-l", f"app={service_name}", "-o", "json"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"✗ Failed to get pods for {service_name}")
        return False

    pods_data = json.loads(result.stdout)
    pods = pods_data.get("items", [])

    if not pods:
        print(f"✗ No pods found for {service_name}")
        return False

    pod = pods[0]
    pod_name = pod["metadata"]["name"]

    # Check containers
    containers = pod["spec"]["containers"]
    container_names = [c["name"] for c in containers]

    has_service = service_name in container_names
    has_dapr = "daprd" in container_names

    # Check pod phase
    phase = pod["status"]["phase"]

    # Check container statuses
    container_statuses = pod["status"].get("containerStatuses", [])
    ready_count = sum(1 for c in container_statuses if c.get("ready", False))
    total_containers = len(container_statuses)

    print(f"Pod: {pod_name}")
    print(f"  Phase: {phase}")
    print(f"  Containers: {ready_count}/{total_containers} ready")
    print(f"  Service container: {'✓' if has_service else '✗'}")
    print(f"  Dapr sidecar: {'✓' if has_dapr else '✗'}")

    if phase == "Running" and ready_count == total_containers and has_dapr:
        print(f"✓ {service_name} is running with Dapr sidecar")
        return True
    else:
        print(f"✗ {service_name} is not fully ready")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_service.py <service_name> [namespace]")
        sys.exit(1)

    service_name = sys.argv[1]
    namespace = sys.argv[2] if len(sys.argv) > 2 else "default"

    success = verify_service(service_name, namespace)
    sys.exit(0 if success else 1)
