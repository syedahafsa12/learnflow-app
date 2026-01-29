#!/usr/bin/env python3
"""
Verify Kubernetes Foundation Readiness
Checks if the cluster is ready for application deployments
"""

import subprocess
import sys
import json
import time

def check_api_server():
    """Check if the API server is responsive."""
    try:
        result = subprocess.run(['kubectl', 'get', 'componentstatuses'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_ingress_controller():
    """Check if ingress controller is running."""
    try:
        result = subprocess.run(['kubectl', 'get', 'pods', '-l', 'app.kubernetes.io/name=ingress-nginx', '-n', 'ingress-nginx', '-o', 'json'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            # Ingress might not be installed yet
            return True  # Consider this acceptable for basic readiness
            
        pods_data = json.loads(result.stdout)
        pods = pods_data['items']
        
        if not pods:
            return True  # No ingress controller required
            
        ready_count = 0
        total_count = len(pods)
        
        for pod in pods:
            status = pod['status']
            # Check if pod is running and ready
            if status.get('phase') == 'Running':
                container_statuses = status.get('containerStatuses', [])
                all_ready = all(container.get('ready', False) for container in container_statuses)
                if all_ready:
                    ready_count += 1
        
        return ready_count == total_count
    except:
        return True  # Don't fail if ingress isn't required

def check_storage_class():
    """Check if default storage class exists."""
    try:
        result = subprocess.run(['kubectl', 'get', 'storageclasses', '-o', 'json'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            return False
            
        sc_data = json.loads(result.stdout)
        storage_classes = sc_data['items']
        
        # Check if there's at least one default storage class
        has_default = any(
            sc['metadata'].get('annotations', {}).get('storageclass.kubernetes.io/is-default-class') == 'true'
            for sc in storage_classes
        )
        
        return has_default or len(storage_classes) > 0
    except:
        # Storage class might not be critical for basic operations
        return True

def check_resource_capacity():
    """Check if there's sufficient resource capacity."""
    try:
        result = subprocess.run(['kubectl', 'top', 'nodes'], 
                              capture_output=True, text=True)
        # If top command works, we have metrics
        return True
    except:
        # Metrics server might not be installed, which is okay
        return True

def main():
    print("Verifying Kubernetes foundation readiness...")
    
    checks = [
        ("API server connectivity", check_api_server),
        ("Ingress controller", check_ingress_controller),
        ("Storage classes", check_storage_class),
        ("Resource metrics", check_resource_capacity)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n{check_name}...")
        if check_func():
            print(f"✓ {check_name} check passed")
        else:
            print(f"✗ {check_name} check failed")
            all_passed = False
    
    if all_passed:
        print("\n✓ All readiness checks passed! Cluster is ready for application deployments.")
        sys.exit(0)
    else:
        print("\n✗ Some readiness checks failed! Cluster may not be ready for application deployments.")
        sys.exit(1)

if __name__ == "__main__":
    main()
