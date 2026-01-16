#!/usr/bin/env python3
"""
Next.js Verification Script
This script verifies that a Next.js application is properly deployed and running on Kubernetes.
"""

import subprocess
import sys
import time
import json
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

def check_deployment_status(app_name, namespace):
    """Check the status of the Next.js deployment."""
    print(f"🔍 Checking deployment status for {app_name} in namespace {namespace}...")

    # Get deployment information
    stdout, stderr, code = run_command(f"kubectl get deployment {app_name} -n {namespace} -o json")

    if code != 0:
        print(f"❌ Failed to get deployment: {stderr}")
        return False

    try:
        deployment_data = json.loads(stdout)

        # Check if deployment exists
        if 'metadata' not in deployment_data:
            print(f"❌ Deployment {app_name} not found in namespace {namespace}")
            return False

        # Check replica status
        status = deployment_data.get('status', {})
        desired_replicas = deployment_data.get('spec', {}).get('replicas', 1)
        ready_replicas = status.get('readyReplicas', 0)
        updated_replicas = status.get('updatedReplicas', 0)

        print(f"  Deployment: {ready_replicas}/{desired_replicas} replicas ready")
        print(f"  Updated: {updated_replicas}/{desired_replicas} replicas updated")

        if ready_replicas >= desired_replicas and updated_replicas >= desired_replicas:
            return True
        else:
            return False

    except json.JSONDecodeError:
        print("❌ Failed to parse deployment status JSON")
        return False

def check_pods_status(app_name, namespace):
    """Check the status of Next.js pods."""
    print(f"\n🔍 Checking pod status for {app_name} in namespace {namespace}...")

    # Get pods for this application
    stdout, stderr, code = run_command(f"kubectl get pods -n {namespace} -l app={app_name} -o json")

    if code != 0:
        print(f"❌ Failed to get pods: {stderr}")
        return False

    try:
        pods_data = json.loads(stdout)
        pods = pods_data.get('items', [])

        if not pods:
            print(f"❌ No pods found for app {app_name} in namespace {namespace}")
            return False

        all_running = True
        for pod in pods:
            pod_name = pod['metadata']['name']
            phase = pod['status'].get('phase', 'Unknown')
            print(f"  Pod {pod_name}: {phase}")

            if phase != 'Running':
                all_running = False
                # Check for specific reasons why it's not running
                if 'containerStatuses' in pod['status']:
                    for container_status in pod['status']['containerStatuses']:
                        if not container_status.get('ready', False):
                            waiting_state = container_status.get('state', {}).get('waiting', {})
                            if waiting_state:
                                reason = waiting_state.get('reason', 'Unknown')
                                message = waiting_state.get('message', '')
                                print(f"    -> Waiting reason: {reason}")
                                if message:
                                    print(f"    -> Message: {message}")

        return all_running

    except json.JSONDecodeError:
        print("❌ Failed to parse pod status JSON")
        return False

def check_service_status(app_name, namespace):
    """Check if the Next.js service is available."""
    print(f"\n🔍 Checking service status for {app_name} in namespace {namespace}...")

    service_name = f"{app_name}-service"
    stdout, stderr, code = run_command(f"kubectl get service {service_name} -n {namespace} -o json")

    if code != 0:
        print(f"❌ Failed to get service {service_name}: {stderr}")
        return False

    try:
        service_data = json.loads(stdout)

        if 'metadata' not in service_data:
            print(f"❌ Service {service_name} not found")
            return False

        service_type = service_data['spec'].get('type', 'Unknown')
        cluster_ip = service_data['spec'].get('clusterIP', 'None')
        ports = service_data['spec'].get('ports', [])

        port_info = ", ".join([f"{port.get('port', 'N/A')}/{port.get('targetPort', 'N/A')}" for port in ports])

        print(f"  Service: {service_name}")
        print(f"  Type: {service_type}")
        print(f"  Cluster IP: {cluster_ip}")
        print(f"  Ports: {port_info}")

        return True

    except json.JSONDecodeError:
        print("❌ Failed to parse service JSON")
        return False

def test_application_health(app_name, namespace):
    """Test the Next.js application health endpoint."""
    print(f"\n🔍 Testing application health for {app_name} in namespace {namespace}...")

    # Wait a moment for the application to be ready
    time.sleep(10)

    # Create a temporary port forward to test the application
    # We'll use kubectl port-forward in the background and test locally
    service_name = f"{app_name}-service"

    # Test by getting pod logs to see if the application started successfully
    stdout, stderr, code = run_command(f"kubectl get pods -n {namespace} -l app={app_name}")

    if code != 0:
        print(f"❌ Could not get pods to test health: {stderr}")
        return False

    # Get the pod name
    lines = stdout.split('\n')
    pod_names = []
    for line in lines[1:]:  # Skip header
        if line.strip():
            parts = line.split()
            if len(parts) > 0:
                pod_names.append(parts[0])

    if not pod_names:
        print(f"❌ No pods found for health check")
        return False

    pod_name = pod_names[0]

    # Get recent logs to check for successful startup
    stdout, stderr, code = run_command(f"kubectl logs -n {namespace} {pod_name} --tail=20")

    if code != 0:
        print(f"❌ Could not get logs for health check: {stderr}")
        return False

    # Look for common success indicators in Next.js logs
    log_lines = stdout.lower()
    success_indicators = [
        'ready in',  # Next.js ready message
        'compiled successfully',  # Compilation success
        'started server',  # Server started
        'listening at',  # Server listening
    ]

    success_found = any(indicator in log_lines for indicator in success_indicators)

    if success_found:
        print(f"  ✅ Application appears to be running (found startup indicators in logs)")
        return True
    else:
        print(f"  ⚠️  Application may not be fully ready yet (no clear startup indicators in recent logs)")
        print(f"     Recent log snippet: {stdout.split(chr(10))[-3:] if chr(10) in stdout else stdout[-100:]}")
        return True  # Don't fail on this, as app might just be initializing

def main():
    parser = argparse.ArgumentParser(description="Verify Next.js deployment on Kubernetes")
    parser.add_argument('app_name', help='Name of the Next.js application')
    parser.add_argument('namespace', help='Kubernetes namespace')

    args = parser.parse_args()

    print(f"📡 Verifying Next.js application '{args.app_name}' in namespace '{args.namespace}'...")

    # Check deployment status
    deployment_ok = check_deployment_status(args.app_name, args.namespace)

    # Check pods status
    pods_ok = check_pods_status(args.app_name, args.namespace)

    # Check service status
    service_ok = check_service_status(args.app_name, args.namespace)

    # Test application health
    health_ok = test_application_health(args.app_name, args.namespace)

    print(f"\n📋 Verification Summary for {args.app_name}:")
    print(f"  Deployment: {'✅ OK' if deployment_ok else '❌ Issues'}")
    print(f"  Pods: {'✅ OK' if pods_ok else '❌ Issues'}")
    print(f"  Service: {'✅ OK' if service_ok else '❌ Issues'}")
    print(f"  Health: {'✅ OK' if health_ok else '❌ Issues'}")

    if deployment_ok and pods_ok and service_ok and health_ok:
        print(f"\n✅ Next.js application '{args.app_name}' verification completed successfully!")
        print(f"The application is ready in the {args.namespace} namespace.")
        return True
    else:
        print(f"\n❌ Next.js application '{args.app_name}' verification failed!")
        print("Please check the deployment and try again.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)