#!/usr/bin/env python3
"""
PostgreSQL Verification Script
Verifies that PostgreSQL is properly deployed and accessible
"""

import subprocess
import json
import sys
import time

def check_postgres_pod():
    """Check if PostgreSQL pod is running."""
    try:
        result = subprocess.run([
            "kubectl", "get", "pods", 
            "-n", "postgresql", 
            "-l", "app.kubernetes.io/name=postgresql",
            "-o", "json"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"FAILED Error getting PostgreSQL pods: {result.stderr}")
            return False

        pods_data = json.loads(result.stdout)
        pods = pods_data["items"]

        if not pods:
            print("FAILED No PostgreSQL pods found")
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
            print(f"SUCCESS All {total_count} PostgreSQL pods are running and ready")
            return True
        else:
            print(f"FAILED {running_count}/{total_count} PostgreSQL pods are running and ready")
            return False

    except Exception as e:
        print(f"FAILED Error checking PostgreSQL pods: {str(e)}")
        return False

def check_postgres_service():
    """Check if PostgreSQL service is available."""
    try:
        result = subprocess.run([
            "kubectl", "get", "svc", 
            "-n", "postgresql", 
            "-l", "app.kubernetes.io/name=postgresql"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"FAILED Error getting PostgreSQL service: {result.stderr}")
            return False

        if "postgresql" in result.stdout:
            print("SUCCESS PostgreSQL service is available")
            return True
        else:
            print("FAILED PostgreSQL service not found")
            return False

    except Exception as e:
        print(f"FAILED Error checking PostgreSQL service: {str(e)}")
        return False

def test_database_connection():
    """Test if we can connect to the database and run queries."""
    try:
        # Wait a bit to ensure PostgreSQL is fully ready
        time.sleep(10)
        
        # Test basic connection and run a simple query
        result = subprocess.run([
            "kubectl", "exec",
            "-n", "postgresql",
            "svc/postgresql",
            "--",
            "psql", "-U", "postgres", "-d", "learnflow_db", "-c", "SELECT version();"
        ], capture_output=True, text=True)

        if result.returncode == 0 and "PostgreSQL" in result.stdout:
            print("SUCCESS Successfully connected to PostgreSQL database")
            return True
        else:
            print(f"FAILED Failed to connect to PostgreSQL database: {result.stderr}")
            return False

    except Exception as e:
        print(f"FAILED Error testing database connection: {str(e)}")
        return False

def check_tables_exist():
    """Check if the expected tables exist."""
    try:
        # Check if our migrated tables exist
        result = subprocess.run([
            "kubectl", "exec",
            "-n", "postgresql",
            "svc/postgresql",
            "--",
            "psql", "-U", "postgres", "-d", "learnflow_db", "-c", 
            "\dt"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            tables = ["users", "modules", "lessons", "exercises", "user_progress", "submissions", "ai_interactions"]
            found_tables = 0
            
            for table in tables:
                if table in result.stdout:
                    found_tables += 1
            
            if found_tables >= len(tables) * 0.7:  # At least 70% of expected tables
                print(f"SUCCESS Found {found_tables}/{len(tables)} expected database tables")
                return True
            else:
                print(f"FAILED Only found {found_tables}/{len(tables)} expected database tables")
                return False
        else:
            print(f"FAILED Failed to list database tables: {result.stderr}")
            return False

    except Exception as e:
        print(f"FAILED Error checking database tables: {str(e)}")
        return False

def main():
    print("Verifying PostgreSQL deployment...")

    checks = [
        ("PostgreSQL pod", check_postgres_pod),
        ("PostgreSQL service", check_postgres_service),
        ("Database connection", test_database_connection),
        ("Tables existence", check_tables_exist)
    ]

    all_passed = True

    for check_name, check_func in checks:
        print(f"\n{check_name}...")
        if not check_func():
            all_passed = False

    if all_passed:
        print("\nSUCCESS PostgreSQL verification successful! Database is ready.")
        sys.exit(0)
    else:
        print("\nFAILED PostgreSQL verification failed! Database is not ready.")
        sys.exit(1)

if __name__ == "__main__":
    main()
