#!/usr/bin/env python3
"""
FastAPI Dapr Service Verification Script
Verifies that the service is properly deployed with Dapr integration
"""

import subprocess
import json
import sys
import time
import requests

def check_service_deployment(service_name):
    """Check if the service deployment is successful."""
    try:
        result = subprocess.run([
            "kubectl", "get", "deployments",
            "-l", f"app={service_name}",
            "-o", "json"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Error getting deployment: {result.stderr}")
            return False

        deployments_data = json.loads(result.stdout)
        deployments = deployments_data["items"]

        if not deployments:
            print(f"✗ No deployment found for service {service_name}")
            return False

        deployment = deployments[0]
        status = deployment.get("status", {})
        spec = deployment.get("spec", {})

        desired_replicas = spec.get("replicas", 0)
        ready_replicas = status.get("readyReplicas", 0)
        updated_replicas = status.get("updatedReplicas", 0)

        if ready_replicas == desired_replicas and updated_replicas == desired_replicas:
            print(f"✓ Service deployment {service_name} is ready ({ready_replicas}/{desired_replicas} replicas)")
            return True
        else:
            print(f"✗ Service deployment not ready: {ready_replicas}/{desired_replicas} ready, {updated_replicas}/{desired_replicas} updated")
            return False

    except Exception as e:
        print(f"✗ Error checking deployment: {str(e)}")
        return False

def check_service_exists(service_name):
    """Check if the service exists and is accessible."""
    try:
        result = subprocess.run([
            "kubectl", "get", "svc",
            f"{service_name}-service",
            "-o", "json"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Error getting service: {result.stderr}")
            return False

        service_data = json.loads(result.stdout)
        service_name_found = service_data["metadata"]["name"]

        if service_name_found:
            print(f"✓ Service {service_name}-service exists")
            return True
        else:
            print(f"✗ Service {service_name}-service not found")
            return False

    except Exception as e:
        print(f"✗ Error checking service: {str(e)}")
        return False

def check_pods_running(service_name):
    """Check if the service pods are running."""
    try:
        result = subprocess.run([
            "kubectl", "get", "pods",
            "-l", f"app={service_name}",
            "-o", "json"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Error getting pods: {result.stderr}")
            return False

        pods_data = json.loads(result.stdout)
        pods = pods_data["items"]

        if not pods:
            print(f"✗ No pods found for service {service_name}")
            return False

        running_count = 0
        total_count = len(pods)

        for pod in pods:
            phase = pod["status"]["phase"]
            if phase == "Running":
                # Check if all containers are ready
                container_statuses = pod["status"].get("containerStatuses", [])
                if all(container.get("ready", False) for container in container_statuses):
                    running_count += 1

        if running_count == total_count:
            print(f"✓ All {total_count} pods for {service_name} are running and ready")
            return True
        else:
            print(f"✗ {running_count}/{total_count} pods for {service_name} are running and ready")
            return False

    except Exception as e:
        print(f"✗ Error checking pods: {str(e)}")
        return False

def check_dapr_sidecar(service_name):
    """Check if Dapr sidecar is injected and running."""
    try:
        result = subprocess.run([
            "kubectl", "get", "pods",
            "-l", f"app={service_name}",
            "-o", "json"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Error getting pods for Dapr check: {result.stderr}")
            return False

        pods_data = json.loads(result.stdout)
        pods = pods_data["items"]

        if not pods:
            print(f"✗ No pods found for service {service_name}")
            return False

        # Check if Dapr sidecar is present in the pod spec
        for pod in pods:
            containers = pod["spec"]["containers"]
            container_names = [c["name"] for c in containers]

            # Also check annotations for dapr
            annotations = pod["metadata"].get("annotations", {})
            dapr_enabled = annotations.get("dapr.io/enabled", "")

            if dapr_enabled == "true":
                print(f"✓ Dapr sidecar annotation found for {service_name}")
                return True

        print(f"✗ Dapr sidecar not found for {service_name}")
        return False

    except Exception as e:
        print(f"✗ Error checking Dapr sidecar: {str(e)}")
        return False

def check_service_connectivity(service_name):
    """Check if the service is accessible via its external IP."""
    try:
        # Get service details
        result = subprocess.run([
            "kubectl", "get", "svc",
            f"{service_name}-service",
            "-o", "json"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Error getting service details: {result.stderr}")
            return False

        service_data = json.loads(result.stdout)
        service_type = service_data["spec"]["type"]

        if service_type == "LoadBalancer":
            # For minikube, we'll use minikube service command to get the URL
            result = subprocess.run([
                "minikube", "service",
                f"{service_name}-service",
                "--url", "-n", "default"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                service_urls = result.stdout.strip().split('\n')
                if service_urls and service_urls[0]:
                    service_url = service_urls[0]  # Take first URL if multiple
                    # Try to access the service health endpoint
                    try:
                        response = requests.get(f"{service_url}/health", timeout=10)
                        if response.status_code == 200:
                            print(f"✓ Service {service_name} is accessible at {service_url}")
                            return True
                        else:
                            print(f"✗ Service {service_name} returned status {response.status_code}")
                            return False
                    except requests.exceptions.RequestException as e:
                        print(f"✗ Cannot access service {service_name}: {str(e)}")
                        return False
                else:
                    print(f"✗ Could not get external URL for {service_name}")
                    return False
            else:
                print(f"✗ Could not get service URL for {service_name}: {result.stderr}")
                return False
        else:
            print(f"✓ Service {service_name} exists (type: {service_type})")
            return True

    except Exception as e:
        print(f"✗ Error checking service connectivity: {str(e)}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_deployment.py <service_name>")
        sys.exit(1)

    service_name = sys.argv[1]
    print(f"Verifying deployment of service: {service_name}")

    checks = [
        ("Service deployment", lambda: check_service_deployment(service_name)),
        ("Service existence", lambda: check_service_exists(service_name)),
        ("Pods running", lambda: check_pods_running(service_name)),
        ("Dapr sidecar", lambda: check_dapr_sidecar(service_name)),
        ("Service connectivity", lambda: check_service_connectivity(service_name))
    ]

    all_passed = True

    for check_name, check_func in checks:
        print(f"\n{check_name}...")
        if not check_func():
            all_passed = False

    if all_passed:
        print(f"\n✓ Service {service_name} verification successful! All components are ready.")
        sys.exit(0)
    else:
        print(f"\n✗ Service {service_name} verification failed! Some components are not ready.")
        sys.exit(1)

if __name__ == "__main__":
    main()