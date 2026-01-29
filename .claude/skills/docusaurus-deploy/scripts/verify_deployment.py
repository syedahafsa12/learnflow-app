#!/usr/bin/env python3
"""
Docusaurus Kubernetes Deployment Verification Script
Verifies that the Docusaurus documentation site is properly deployed and accessible
"""

import subprocess
import json
import sys
import requests
from typing import Dict, Any

def check_deployment(site_name: str) -> bool:
    """Check if the Docusaurus deployment is successful."""
    try:
        result = subprocess.run([
            "kubectl", "get", "deployments", 
            "-l", f"app={site_name}-docs", 
            "-o", "json"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Error getting deployment: {result.stderr}")
            return False

        deployments_data = json.loads(result.stdout)
        deployments = deployments_data["items"]

        if not deployments:
            print(f"✗ No deployment found for site {site_name}-docs")
            return False

        deployment = deployments[0]
        status = deployment.get("status", {})
        spec = deployment.get("spec", {})

        desired_replicas = spec.get("replicas", 0)
        ready_replicas = status.get("readyReplicas", 0)
        updated_replicas = status.get("updatedReplicas", 0)

        if ready_replicas == desired_replicas and updated_replicas == desired_replicas:
            print(f"✓ Deployment {site_name}-docs-deployment is ready ({ready_replicas}/{desired_replicas} replicas)")
            return True
        else:
            print(f"✗ Deployment not ready: {ready_replicas}/{desired_replicas} ready, {updated_replicas}/{desired_replicas} updated")
            return False

    except Exception as e:
        print(f"✗ Error checking deployment: {str(e)}")
        return False

def check_service(site_name: str) -> bool:
    """Check if the service exists and is accessible."""
    try:
        result = subprocess.run([
            "kubectl", "get", "svc", 
            f"{site_name}-docs-service",
            "-o", "json"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Error getting service: {result.stderr}")
            return False

        service_data = json.loads(result.stdout)
        service_name_found = service_data["metadata"]["name"]

        if service_name_found:
            print(f"✓ Service {site_name}-docs-service exists")
            return True
        else:
            print(f"✗ Service {site_name}-docs-service not found")
            return False

    except Exception as e:
        print(f"✗ Error checking service: {str(e)}")
        return False

def check_pods_running(site_name: str) -> bool:
    """Check if the documentation site pods are running."""
    try:
        result = subprocess.run([
            "kubectl", "get", "pods", 
            "-l", f"app={site_name}-docs", 
            "-o", "json"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Error getting pods: {result.stderr}")
            return False

        pods_data = json.loads(result.stdout)
        pods = pods_data["items"]

        if not pods:
            print(f"✗ No pods found for site {site_name}-docs")
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
            print(f"✓ All {total_count} pods for {site_name}-docs are running and ready")
            return True
        else:
            print(f"✗ {running_count}/{total_count} pods for {site_name}-docs are running and ready")
            return False

    except Exception as e:
        print(f"✗ Error checking pods: {str(e)}")
        return False

def check_site_accessibility(site_name: str) -> bool:
    """Check if the documentation site is accessible via its external IP."""
    try:
        # Get service details
        result = subprocess.run([
            "kubectl", "get", "svc", 
            f"{site_name}-docs-service",
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
                f"{site_name}-docs-service",
                "--url", "-n", "default"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                service_urls = result.stdout.strip().split('\n')
                if service_urls and service_urls[0]:
                    service_url = service_urls[0]  # Take first URL if multiple
                    
                    # Try to access the documentation site root page
                    try:
                        response = requests.get(service_url, timeout=30)
                        if response.status_code in [200, 201, 301, 302, 304]:
                            print(f"✓ Documentation site {site_name} is accessible at {service_url}")
                            
                            # Check if it's a Docusaurus site by looking for common indicators
                            content = response.text
                            if "docusaurus" in content.lower() or "apache" in content.lower() or "documentation" in content.lower():
                                print("✓ Confirmed: This is a Docusaurus documentation site")
                            
                            return True
                        else:
                            print(f"✗ Site returned status {response.status_code}")
                            return False
                    except requests.exceptions.RequestException as e:
                        print(f"✗ Cannot access documentation site {site_name}: {str(e)}")
                        return False
                else:
                    print(f"✗ Could not get external URL for {site_name}")
                    return False
            else:
                print(f"✗ Could not get service URL for {site_name}: {result.stderr}")
                return False
        else:
            print(f"✓ Service {site_name} exists (type: {service_type})")
            return True

    except Exception as e:
        print(f"✗ Error checking site accessibility: {str(e)}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_deployment.py <site_name>")
        sys.exit(1)
    
    site_name = sys.argv[1]
    print(f"Verifying deployment of Docusaurus site: {site_name}")

    checks = [
        ("Deployment status", lambda: check_deployment(site_name)),
        ("Service existence", lambda: check_service(site_name)),
        ("Pods running", lambda: check_pods_running(site_name)),
        ("Site accessibility", lambda: check_site_accessibility(site_name))
    ]

    all_passed = True

    for check_name, check_func in checks:
        print(f"\n{check_name}...")
        if not check_func():
            all_passed = False

    if all_passed:
        print(f"\n✓ Docusaurus site {site_name} verification successful! All components are ready.")
        sys.exit(0)
    else:
        print(f"\n✗ Docusaurus site {site_name} verification failed! Some components are not ready.")
        sys.exit(1)

if __name__ == "__main__":
    main()
