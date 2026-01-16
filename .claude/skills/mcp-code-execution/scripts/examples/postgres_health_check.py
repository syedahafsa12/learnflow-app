#!/usr/bin/env python3
"""
Example: PostgreSQL Health Check using MCP Code Execution Pattern
This script demonstrates how to efficiently check PostgreSQL health
while minimizing token usage in the agent context.
"""

import subprocess
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

def get_postgres_pod():
    """Get the name of the PostgreSQL pod."""
    stdout, stderr, code = run_command("kubectl get pods -n postgres -l app.kubernetes.io/name=postgresql,app.kubernetes.io/component=primary -o jsonpath='{.items[0].metadata.name}'")

    if code != 0 or not stdout:
        return None

    return stdout.strip().strip("'")

def check_postgres_health():
    """Check PostgreSQL health with minimal output."""

    postgres_pod = get_postgres_pod()
    if not postgres_pod:
        return "❌ Cannot find PostgreSQL pod", False

    # Check if PostgreSQL is responsive by running a simple query
    cmd = f'''kubectl exec -n postgres {postgres_pod} -- bash -c "PGPASSWORD=secretpassword psql -h localhost -U postgres -d learnflow -tAc 'SELECT version();'"'''

    stdout, stderr, code = run_command(cmd)

    if code != 0 or "PostgreSQL" not in stdout:
        return f"❌ PostgreSQL not responding: {stderr[:100]}", False

    # Get basic database statistics
    cmd = f'''kubectl exec -n postgres {postgres_pod} -- bash -c "PGPASSWORD=secretpassword psql -h localhost -U postgres -d learnflow -tAc 'SELECT count(*) FROM pg_tables WHERE schemaname = \\'public\\';'"'''

    stdout, stderr, code = run_command(cmd)

    if code != 0:
        return f"⚠️  PostgreSQL responding but cannot query tables: {stderr[:100]}", True

    table_count = int(stdout.strip()) if stdout.strip().isdigit() else 0

    # Get database size
    cmd = f'''kubectl exec -n postgres {postgres_pod} -- bash -c "PGPASSWORD=secretpassword psql -h localhost -U postgres -d learnflow -tAc 'SELECT pg_size_pretty(pg_database_size(current_database()));'"'''

    stdout, stderr, code = run_command(cmd)

    db_size = stdout.strip() if code == 0 and stdout.strip() else "unknown"

    return f"✅ PostgreSQL healthy: version accessible, {table_count} tables in learnflow db, size {db_size}", True

def main():
    """Main function to check PostgreSQL health."""
    print("Checking PostgreSQL health...")

    status_message, is_healthy = check_postgres_health()
    print(status_message)

    # Return exit code based on health status
    sys.exit(0 if is_healthy else 1)

if __name__ == "__main__":
    main()