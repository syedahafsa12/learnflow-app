#!/usr/bin/env python3
"""
PostgreSQL Migration Script
This script runs SQL migration files against the Kubernetes-deployed PostgreSQL database.
"""

import subprocess
import sys
import argparse
import os
from pathlib import Path

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
        print(f"✗ Could not find PostgreSQL pod: {stderr}")
        return None

    return stdout.strip().strip("'")

def execute_sql_file(sql_file_path):
    """Execute a SQL file against the PostgreSQL database."""
    postgres_pod = get_postgres_pod()
    if not postgres_pod:
        return False

    print(f"🔧 Executing migration: {sql_file_path}")

    # Copy the SQL file to the pod temporarily
    copy_cmd = f"kubectl cp {sql_file_path} postgres/{postgres_pod}:/tmp/migration.sql -n postgres"
    stdout, stderr, code = run_command(copy_cmd)

    if code != 0:
        print(f"  ❌ Failed to copy SQL file to pod: {stderr}")
        return False

    # Execute the SQL file in the database
    exec_cmd = f'''kubectl exec -n postgres {postgres_pod} -- bash -c "PGPASSWORD=secretpassword psql -h localhost -U postgres -d learnflow -f /tmp/migration.sql"'''

    stdout, stderr, code = run_command(exec_cmd)

    if code == 0:
        print(f"  ✅ Migration '{sql_file_path}' executed successfully")

        # Clean up the temporary file
        cleanup_cmd = f"kubectl exec -n postgres {postgres_pod} -- rm /tmp/migration.sql"
        run_command(cleanup_cmd)  # Don't check result for cleanup

        return True
    else:
        print(f"  ❌ Failed to execute migration '{sql_file_path}': {stderr}")
        # Clean up the temporary file
        cleanup_cmd = f"kubectl exec -n postgres {postgres_pod} -- rm /tmp/migration.sql"
        run_command(cleanup_cmd)
        return False

def execute_sql_query(query):
    """Execute a single SQL query against the PostgreSQL database."""
    postgres_pod = get_postgres_pod()
    if not postgres_pod:
        return False

    exec_cmd = f'''kubectl exec -n postgres {postgres_pod} -- bash -c "PGPASSWORD=secretpassword psql -h localhost -U postgres -d learnflow -c \\\"{query}\\\""'''

    stdout, stderr, code = run_command(exec_cmd)

    if code == 0:
        print(f"Query executed successfully: {query[:50]}...")
        return True, stdout
    else:
        print(f"Failed to execute query: {stderr}")
        return False, stderr

def list_tables():
    """List all tables in the database."""
    postgres_pod = get_postgres_pod()
    if not postgres_pod:
        return False

    print("📋 Current tables in database:")

    query = r"\dt"
    exec_cmd = f'''kubectl exec -n postgres {postgres_pod} -- bash -c "PGPASSWORD=secretpassword psql -h localhost -U postgres -d learnflow -c \\\"{query}\\\""'''

    stdout, stderr, code = run_command(exec_cmd)

    if code == 0:
        # Filter out the header and footer, just show table names
        lines = stdout.split('\n')
        table_lines = [line for line in lines if '|' in line and 'List' not in line]
        for line in table_lines:
            if line.strip():
                print(f"  - {line.split('|')[1].strip()}")
        return True
    else:
        print(f"  ❌ Failed to list tables: {stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run PostgreSQL migrations in Kubernetes")
    parser.add_argument('migration_files', nargs='+', help='SQL migration files to execute')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be executed without running')
    parser.add_argument('--list-tables', action='store_true', help='List existing tables')

    args = parser.parse_args()

    if args.list_tables:
        list_tables()
        return

    if args.dry_run:
        print("🔍 Dry run mode - showing what would be executed:")
        for migration_file in args.migration_files:
            print(f"  - Would execute: {migration_file}")
        return

    # Validate that migration files exist
    valid_files = []
    for migration_file in args.migration_files:
        path = Path(migration_file)
        if not path.exists():
            print(f"❌ Migration file does not exist: {migration_file}")
            continue
        if path.suffix.lower() != '.sql':
            print(f"⚠️  Migration file is not .sql: {migration_file}")
        valid_files.append(path)

    if not valid_files:
        print("❌ No valid migration files found!")
        return 1

    print(f"📡 Running {len(valid_files)} migration(s)...")

    success_count = 0
    for sql_file in valid_files:
        if execute_sql_file(str(sql_file)):
            success_count += 1

    print(f"\n📊 Summary: {success_count}/{len(valid_files)} migrations executed successfully")

    # List tables after migration
    print("\n📈 Updated table list:")
    list_tables()

    if success_count == len(valid_files):
        print("\n✅ All migrations completed successfully!")
        return 0
    else:
        print(f"\n⚠️  Some migrations failed ({success_count}/{len(valid_files)} succeeded)")
        return 1

if __name__ == "__main__":
    sys.exit(main())