#!/usr/bin/env python3
"""
Kubernetes Cluster Health Check
Checks the basic health of a Kubernetes cluster
"""

import subprocess
import sys
import json

def check_kubectl_connection():
    """Check if kubectl can connect to the cluster."""
    try:
        result = subprocess.run(['kubectl', 'cluster-info'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("✗ kubectl connection timed out")
        return False
    except FileNotFoundError:
        print("✗ kubectl command not found")
        return False

def check_nodes_status():
    """Check the status of all nodes."""
    try:
        result = subprocess.run(['kubectl', 'get', 'nodes', '-o', 'json'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"✗ Failed to get nodes: {result.stderr}")
            return False
            
        nodes_data = json.loads(result.stdout)
        nodes = nodes_data['items']
        
        ready_count = 0
        total_count = len(nodes)
        
        for node in nodes:
            conditions = node['status'].get('conditions', [])
            for condition in conditions:
                if condition['type'] == 'Ready':
                    if condition['status'] == 'True':
                        ready_count += 1
                    break
        
        if ready_count == total_count:
            print(f"✓ All {total_count} nodes are ready")
            return True
        else:
            print(f"✗ {ready_count}/{total_count} nodes are ready")
            return False
    except Exception as e:
        print(f"✗ Error checking nodes: {str(e)}")
        return False

def check_core_components():
    """Check status of core Kubernetes components."""
    try:
        # Check kube-system pods
        result = subprocess.run(['kubectl', 'get', 'pods', '-n', 'kube-system', '-o', 'json'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"✗ Failed to get kube-system pods: {result.stderr}")
            return False
            
        pods_data = json.loads(result.stdout)
        pods = pods_data['items']
        
        running_count = 0
        total_count = len(pods)
        
        for pod in pods:
            phase = pod['status'].get('phase', 'Unknown')
            if phase in ['Running', 'Succeeded']:
                running_count += 1
        
        if running_count >= total_count * 0.9:  # At least 90% running
            print(f"✓ {running_count}/{total_count} kube-system pods are running")
            return True
        else:
            print(f"✗ Only {running_count}/{total_count} kube-system pods are running")
            return False
    except Exception as e:
        print(f"✗ Error checking core components: {str(e)}")
        return False

def main():
    print("Checking Kubernetes cluster health...")
    
    checks = [
        ("kubectl connection", check_kubectl_connection),
        ("nodes status", check_nodes_status),
        ("core components", check_core_components)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n{check_name}...")
        if not check_func():
            all_passed = False
    
    if all_passed:
        print("\n✓ Cluster health check passed!")
        sys.exit(0)
    else:
        print("\n✗ Cluster health check failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
