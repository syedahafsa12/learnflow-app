#!/usr/bin/env python3
"""
MCP Client Script
This script demonstrates the MCP Code Execution pattern by wrapping MCP calls in scripts
to reduce token usage while maintaining full functionality.
"""

import subprocess
import sys
import json
import argparse
from pathlib import Path

def run_shell_command(command):
    """Execute a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip(), result.stderr.strip(), 0
    except subprocess.CalledProcessError as e:
        return e.stdout.strip(), e.stderr.strip(), e.returncode

def kubernetes_operation(operation, resource_type, resource_name=None, namespace="default", filters=None):
    """
    Perform Kubernetes operations via MCP-style calls.

    This function demonstrates the code execution pattern where
    the MCP interaction happens in the script (outside context),
    and only minimal results return to the agent.
    """
    if operation == "get":
        if resource_name:
            cmd = f"kubectl get {resource_type} {resource_name} -n {namespace} -o json"
        else:
            cmd = f"kubectl get {resource_type} -n {namespace} -o json"

        stdout, stderr, code = run_shell_command(cmd)

        if code != 0:
            return f"Error getting {resource_type}: {stderr}", False

        try:
            data = json.loads(stdout)

            # Apply filters if provided
            if filters and isinstance(data, dict) and 'items' in data:
                # Filter the items based on provided criteria
                filtered_items = []
                for item in data['items']:
                    matches = True
                    for key, value in filters.items():
                        # Navigate nested keys like 'status.phase' or 'metadata.name'
                        item_value = item
                        for k in key.split('.'):
                            item_value = item_value.get(k, {}) if isinstance(item_value, dict) else {}

                        if isinstance(item_value, dict) and value in str(item_value):
                            continue
                        elif str(item_value) != str(value):
                            matches = False
                            break

                    if matches:
                        filtered_items.append(item)

                data['items'] = filtered_items

            # Return minimal summary instead of full JSON
            if resource_name:
                # Single resource - return simple status
                if 'status' in data and 'phase' in data['status']:
                    return f"{resource_type}/{resource_name} in namespace {namespace} is {data['status']['phase']}", True
                else:
                    return f"{resource_type}/{resource_name} found in namespace {namespace}", True
            else:
                # Multiple resources - return count and brief status
                if 'items' in data:
                    items = data['items']
                    statuses = {}
                    for item in items:
                        if 'status' in item and 'phase' in item['status']:
                            status = item['status']['phase']
                            statuses[status] = statuses.get(status, 0) + 1
                        else:
                            statuses['unknown'] = statuses.get('unknown', 0) + 1

                    status_str = ", ".join([f"{count} {status}" for status, count in statuses.items()])
                    return f"Found {len(items)} {resource_type} in namespace {namespace}: {status_str}", True
                else:
                    return f"Found {resource_type} in namespace {namespace}", True

        except json.JSONDecodeError:
            # If JSON parsing fails, return a simple success message
            return f"Retrieved {resource_type} from namespace {namespace}", True

    elif operation == "describe":
        if not resource_name:
            return "Resource name required for describe operation", False

        cmd = f"kubectl describe {resource_type} {resource_name} -n {namespace}"
        stdout, stderr, code = run_shell_command(cmd)

        if code != 0:
            return f"Error describing {resource_type}/{resource_name}: {stderr}", False

        # Return only key information, not full verbose output
        lines = stdout.split('\n')
        key_info = []
        for line in lines:
            # Extract only important status information
            if any(keyword in line.lower() for keyword in ['status:', 'phase:', 'ready', 'running', 'error', 'failed']):
                key_info.append(line.strip())

        if key_info:
            return f"{resource_type}/{resource_name} status:\n" + "\n".join(key_info[:5]), True  # Limit to 5 lines
        else:
            return f"{resource_type}/{resource_name} described successfully", True

def kafka_operation(operation, topic_name=None, namespace="kafka"):
    """
    Perform Kafka operations via MCP-style calls.
    Demonstrates code execution pattern for message queue operations.
    """
    if operation == "list_topics":
        cmd = f"kubectl exec -n {namespace} -it $(kubectl get pods -n {namespace} -l app.kubernetes.io/name=kafka -o jsonpath='{{.items[0].metadata.name}}') -- kafka-topics.sh --list --bootstrap-server localhost:9092"
        stdout, stderr, code = run_shell_command(cmd)

        if code != 0:
            return f"Error listing Kafka topics: {stderr}", False

        topics = [t.strip() for t in stdout.split('\n') if t.strip()]
        return f"Found {len(topics)} Kafka topics: {', '.join(topics[:10])}{'...' if len(topics) > 10 else ''}", True

    elif operation == "describe_topic" and topic_name:
        cmd = f"kubectl exec -n {namespace} -it $(kubectl get pods -n {namespace} -l app.kubernetes.io/name=kafka -o jsonpath='{{.items[0].metadata.name}}') -- kafka-topics.sh --describe --topic {topic_name} --bootstrap-server localhost:9092"
        stdout, stderr, code = run_shell_command(cmd)

        if code != 0:
            return f"Error describing topic {topic_name}: {stderr}", False

        # Parse and summarize topic info
        lines = stdout.split('\n')
        summary = []
        for line in lines:
            if 'PartitionCount' in line or 'ReplicationFactor' in line or 'Leader' in line:
                summary.append(line.strip())

        if summary:
            return f"Topic {topic_name}:\n" + "\n".join(summary[:3]), True  # Limit to 3 lines
        else:
            return f"Topic {topic_name} described", True

def postgresql_operation(operation, query=None, namespace="postgres"):
    """
    Perform PostgreSQL operations via MCP-style calls.
    Demonstrates code execution pattern for database operations.
    """
    if operation == "execute_query" and query:
        # Execute query and return summary
        cmd = f'''kubectl exec -n {namespace} -it $(kubectl get pods -n {namespace} -l app.kubernetes.io/name=postgresql,app.kubernetes.io/component=primary -o jsonpath='{{.items[0].metadata.name}}') -- bash -c "PGPASSWORD=secretpassword psql -h localhost -U postgres -d learnflow -tAc '{query}'"'''

        stdout, stderr, code = run_shell_command(cmd)

        if code != 0:
            return f"Error executing query: {stderr}", False

        # Return summary of results, not full result set
        lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        if len(lines) > 5:
            return f"Query executed successfully, returning {len(lines)} rows (showing first 5):\n" + "\n".join(lines[:5]) + "\n...", True
        else:
            return f"Query executed successfully, returning {len(lines)} rows:\n" + "\n".join(lines), True

    elif operation == "list_tables":
        cmd = f'''kubectl exec -n {namespace} -it $(kubectl get pods -n {namespace} -l app.kubernetes.io/name=postgresql,app.kubernetes.io/component=primary -o jsonpath='{{.items[0].metadata.name}}') -- bash -c "PGPASSWORD=secretpassword psql -h localhost -U postgres -d learnflow -tAc '\\dt'"'''

        stdout, stderr, code = run_shell_command(cmd)

        if code != 0:
            return f"Error listing tables: {stderr}", False

        lines = [line.strip() for line in stdout.split('\n') if '|' in line and 'List' not in line]
        table_names = [line.split('|')[1].strip() for line in lines if line.strip()]

        return f"Found {len(table_names)} tables in learnflow database: {', '.join(table_names[:10])}{'...' if len(table_names) > 10 else ''}", True

def main():
    parser = argparse.ArgumentParser(description="MCP Client - Code Execution Pattern Demonstration")

    # Common arguments
    parser.add_argument("--system", required=True, choices=["kubernetes", "kafka", "postgresql"],
                       help="Target system for MCP operations")
    parser.add_argument("--operation", required=True,
                       help="Operation to perform (get, describe, list_topics, execute_query, etc.)")

    # Resource-specific arguments
    parser.add_argument("--resource-type", help="Resource type (pods, services, etc.)")
    parser.add_argument("--resource-name", help="Specific resource name")
    parser.add_argument("--namespace", default="default", help="Kubernetes namespace")
    parser.add_argument("--topic", help="Kafka topic name")
    parser.add_argument("--query", help="SQL query to execute")
    parser.add_argument("--filter", action='append', help="Filter in format key=value")

    args = parser.parse_args()

    # Parse filters
    filters = {}
    if args.filter:
        for f in args.filter:
            if '=' in f:
                key, value = f.split('=', 1)
                filters[key] = value

    # Route to appropriate handler
    if args.system == "kubernetes":
        if not args.resource_type:
            print("Error: --resource-type is required for Kubernetes operations", file=sys.stderr)
            sys.exit(1)

        result, success = kubernetes_operation(
            args.operation,
            args.resource_type,
            args.resource_name,
            args.namespace,
            filters if filters else None
        )

    elif args.system == "kafka":
        topic_name = args.topic or args.resource_name
        result, success = kafka_operation(args.operation, topic_name, args.namespace)

    elif args.system == "postgresql":
        query = args.query
        result, success = postgresql_operation(args.operation, query, args.namespace)

    # Output minimal result to context
    print(result)

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()