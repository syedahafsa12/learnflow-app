#!/usr/bin/env python3
"""
MCP Client for Code Execution Pattern
Demonstrates how to wrap MCP calls in efficient code execution
"""

import json
import os
import sys
import requests
from typing import Any, Dict, List, Optional

class MCPClient:
    """
    MCP Client that demonstrates the code execution pattern for efficient token usage.
    Instead of returning large datasets directly to the agent context, this client
    processes data internally and returns only the necessary results.
    """
    
    def __init__(self, server_url: Optional[str] = None):
        """
        Initialize the MCP client.
        
        Args:
            server_url: URL of the MCP server. If None, looks for MCP_SERVER_URL env var
        """
        self.server_url = server_url or os.environ.get('MCP_SERVER_URL')
        if not self.server_url:
            raise ValueError("MCP server URL must be provided either as parameter or MCP_SERVER_URL environment variable")
    
    def get_large_dataset(self, dataset_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve a large dataset from MCP server.
        This would normally return thousands of rows to context, causing token bloat.
        Instead, we process it here and return only what's needed.
        """
        # Simulate MCP call - in real implementation this would call the MCP server
        print(f"Simulating retrieval of large dataset: {dataset_id}")
        
        # Generate sample data to simulate what we might get from MCP
        sample_data = []
        for i in range(1000):  # Simulate 1000 records
            sample_data.append({
                "id": i,
                "name": f"Record {i}",
                "status": "active" if i % 3 != 0 else "inactive",
                "value": i * 10,
                "category": f"Category_{i % 10}"
            })
        
        return sample_data
    
    def filter_and_summarize(self, dataset_id: str, filter_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Efficiently filter and summarize a large dataset.
        Instead of returning all data to agent context, process it here.
        
        Args:
            dataset_id: ID of the dataset to process
            filter_criteria: Dictionary specifying how to filter the data
            
        Returns:
            Summary of filtered results
        """
        print(f"Filtering dataset {dataset_id} with criteria: {filter_criteria}")
        
        # Get the dataset
        full_dataset = self.get_large_dataset(dataset_id)
        
        # Apply filtering based on criteria
        filtered_data = []
        for record in full_dataset:
            matches = True
            for key, value in filter_criteria.items():
                if key not in record or record[key] != value:
                    matches = False
                    break
            if matches:
                filtered_data.append(record)
        
        # Return only the summary, not the full dataset
        summary = {
            "total_records": len(full_dataset),
            "filtered_count": len(filtered_data),
            "sample_records": filtered_data[:5],  # Only first 5 records
            "summary_stats": {
                "active_count": len([r for r in filtered_data if r.get("status") == "active"]),
                "inactive_count": len([r for r in filtered_data if r.get("status") == "inactive"]),
                "avg_value": sum(r.get("value", 0) for r in filtered_data) / max(len(filtered_data), 1)
            }
        }
        
        return summary
    
    def aggregate_data(self, dataset_id: str, group_by_field: str) -> Dict[str, Any]:
        """
        Aggregate data by a specific field.
        Returns grouped statistics instead of raw data.
        
        Args:
            dataset_id: ID of the dataset to process
            group_by_field: Field to group data by
            
        Returns:
            Aggregated statistics
        """
        print(f"Aggregating dataset {dataset_id} by field: {group_by_field}")
        
        # Get the dataset
        full_dataset = self.get_large_dataset(dataset_id)
        
        # Group and aggregate
        groups = {}
        for record in full_dataset:
            key = record.get(group_by_field, "unknown")
            if key not in groups:
                groups[key] = {
                    "count": 0,
                    "values": [],
                    "active_count": 0
                }
            groups[key]["count"] += 1
            groups[key]["values"].append(record.get("value", 0))
            if record.get("status") == "active":
                groups[key]["active_count"] += 1
        
        # Calculate aggregates
        result = {}
        for key, data in groups.items():
            result[key] = {
                "count": data["count"],
                "active_percentage": (data["active_count"] / data["count"]) * 100,
                "avg_value": sum(data["values"]) / len(data["values"]) if data["values"] else 0,
                "max_value": max(data["values"]) if data["values"] else 0,
                "min_value": min(data["values"]) if data["values"] else 0
            }
        
        return result

def main():
    """
    Main function demonstrating the MCP Code Execution Pattern.
    Shows how to process large datasets efficiently without bloating context.
    """
    print("MCP Code Execution Pattern Demonstration")
    print("=" * 50)
    
    # Initialize client
    try:
        client = MCPClient(server_url="http://mock-mcp-server")  # In real use, this would be actual MCP server
    except ValueError as e:
        print(f"Error initializing MCP client: {e}")
        return 1
    
    # Example 1: Filter and summarize large dataset (token-efficient approach)
    print("\n1. Efficient filtering (only summary returned to context):")
    filter_result = client.filter_and_summarize(
        dataset_id="student_progress", 
        filter_criteria={"status": "active"}
    )
    print(json.dumps(filter_result, indent=2))
    
    # Example 2: Aggregate data by category
    print("\n2. Data aggregation (only stats returned to context):")
    agg_result = client.aggregate_data(
        dataset_id="student_performance",
        group_by_field="category"
    )
    print(json.dumps(agg_result, indent=2))
    
    print("\n✓ MCP Code Execution Pattern demonstration completed!")
    print("Notice: Only summaries and aggregated data returned to context, not full datasets.")
    print("This significantly reduces token consumption compared to direct MCP calls.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
