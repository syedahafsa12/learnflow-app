#!/usr/bin/env python3
"""
Example: Kubernetes Health Check using MCP Code Execution Pattern
This script demonstrates how to efficiently check cluster health
while minimizing token usage in the agent context.
"""

import subprocess
import json
import sys

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

def check_cluster_health():
    """Check overall cluster health with minimal output."""

    # Check nodes status
    stdout, stderr, code = run_command("kubectl get nodes -o json")
    if code != 0:
        return "❌ Cannot access cluster nodes", False

    try:
        nodes_data = json.loads(stdout)
        nodes = nodes_data.get('items', [])

        ready_nodes = 0
        total_nodes = len(nodes)

        for node in nodes:
            conditions = node.get('status', {}).get('conditions', [])
            for condition in conditions:
                if condition.get('type') == 'Ready':
                    if condition.get('status') == 'True':
                        ready_nodes += 1
                    break

        # Check system pods
        stdout, stderr, code = run_command("kubectl get pods -n kube-system -o json")
        if code != 0:
            return f"✅ {ready_nodes}/{total_nodes} nodes ready, but kube-system inaccessible", False

        pods_data = json.loads(stdout)
        pods = pods_data.get('items', [])

        system_pods_ready = 0
        total_system_pods = len(pods)

        for pod in pods:
            status = pod.get('status', {})
            phase = status.get('phase')
            if phase == 'Running':
                container_statuses = status.get('containerStatuses', [])
                ready_containers = sum(1 for cs in container_statuses if cs.get('ready', False))
                total_containers = len(container_statuses)

                if container_statuses and ready_containers == total_containers:
                    system_pods_ready += 1

        # Generate summary
        node_status = f"{ready_nodes}/{total_nodes} nodes ready"
        pod_status = f"{system_pods_ready}/{total_system_pods} system pods ready"

        if ready_nodes == total_nodes and system_pods_ready >= total_system_pods * 0.8:  # 80% threshold
            return f"✅ Cluster healthy: {node_status}, {pod_status}", True
        else:
            return f"⚠️  Cluster issues: {node_status}, {pod_status}", False

    except json.JSONDecodeError:
        return "❌ Cannot parse cluster status", False

def main():
    """Main function to check cluster health."""
    print("Checking Kubernetes cluster health...")

    status_message, is_healthy = check_cluster_health()
    print(status_message)

    # Return exit code based on health status
    sys.exit(0 if is_healthy else 1)

if __name__ == "__main__":
    main()