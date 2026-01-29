#!/usr/bin/env python3
"""
MCP Integration Demo
Shows various patterns for integrating MCP with code execution
"""

import json
import sys
from typing import Any, Dict, List

def demonstrate_token_efficiency():
    """Demonstrate the token efficiency of code execution pattern."""
    print("Token Efficiency Demonstration")
    print("-" * 30)
    
    # Simulate large data that would come from MCP
    large_dataset = []
    for i in range(5000):  # 5000 records
        large_dataset.append({
            "id": i,
            "student_id": f"student_{i}",
            "exercise_id": f"exercise_{i % 100}",
            "score": (i * 7) % 100,
            "timestamp": f"2023-12-{(i % 30) + 1:02d}",
            "status": "completed" if i % 2 == 0 else "in_progress"
        })
    
    print(f"Generated large dataset: {len(large_dataset)} records")
    print(f"Raw data size: ~{len(json.dumps(large_dataset))} characters")
    
    # Instead of returning the full dataset to agent context (token bloat),
    # process it here and return only insights
    insights = {
        "total_students": len(large_dataset),
        "completion_rate": len([r for r in large_dataset if r["status"] == "completed"]) / len(large_dataset),
        "average_score": sum(r["score"] for r in large_dataset) / len(large_dataset),
        "struggling_students": [r for r in large_dataset if r["score"] < 50][:10],  # Only top 10 struggling
        "high_performers": [r for r in large_dataset if r["score"] > 90][:10]  # Only top 10 performers
    }
    
    print(f"Processed insights size: ~{len(json.dumps(insights))} characters")
    print(f"Token reduction: ~{100 - (len(json.dumps(insights)) / len(json.dumps(large_dataset)) * 100):.1f}%")
    
    return insights

def demonstrate_filtering_pattern():
    """Demonstrate the filtering pattern."""
    print("\nFiltering Pattern Demonstration")
    print("-" * 35)
    
    # Simulate data from MCP
    raw_data = [{"id": i, "type": "error" if i % 7 == 0 else "success", "msg": f"Message {i}"} for i in range(1000)]
    
    # Instead of returning all 1000 records, filter to relevant ones
    error_messages = [item for item in raw_data if item["type"] == "error"]
    
    print(f"Original data: {len(raw_data)} records")
    print(f"Filtered data: {len(error_messages)} error records")
    print(f"Reduction: {len(raw_data) - len(error_messages)} irrelevant records excluded from context")
    
    return error_messages

def demonstrate_aggregation_pattern():
    """Demonstrate the aggregation pattern."""
    print("\nAggregation Pattern Demonstration")
    print("-" * 35)
    
    # Simulate student exercise data from MCP
    exercise_data = []
    for i in range(2000):
        exercise_data.append({
            "exercise_id": f"ex_{i % 50}",  # 50 different exercises
            "student_id": f"student_{i % 200}",  # 200 different students
            "score": (i * 3) % 100,
            "attempts": (i % 5) + 1
        })
    
    # Aggregate data instead of returning raw records
    exercise_scores = {}
    for record in exercise_data:
        ex_id = record["exercise_id"]
        if ex_id not in exercise_scores:
            exercise_scores[ex_id] = {"scores": [], "attempts": []}
        exercise_scores[ex_id]["scores"].append(record["score"])
        exercise_scores[ex_id]["attempts"].append(record["attempts"])
    
    # Calculate averages
    aggregated = {}
    for ex_id, data in exercise_scores.items():
        aggregated[ex_id] = {
            "average_score": sum(data["scores"]) / len(data["scores"]),
            "average_attempts": sum(data["attempts"]) / len(data["attempts"]),
            "completion_count": len(data["scores"])
        }
    
    print(f"Original data: {len(exercise_data)} records")
    print(f"Aggregated data: {len(aggregated)} exercise summaries")
    print(f"Reduction: Processed {len(exercise_data)} records into {len(aggregated)} insights")
    
    return aggregated

def main():
    """Main function demonstrating MCP integration patterns."""
    print("MCP Integration Patterns Demo")
    print("=" * 40)
    
    # Demonstrate token efficiency
    insights = demonstrate_token_efficiency()
    
    # Demonstrate filtering
    errors = demonstrate_filtering_pattern()
    
    # Demonstrate aggregation
    agg_data = demonstrate_aggregation_pattern()
    
    print(f"\n✓ MCP Integration Patterns Demo Completed!")
    print(f"Patterns demonstrated:")
    print(f"  - Token-efficient processing: {len(insights)} insights from large dataset")
    print(f"  - Filtering pattern: {len(errors)} relevant items from {len(errors) + 900} total")
    print(f"  - Aggregation pattern: {len(agg_data)} summaries from 2000 records")
    print(f"All patterns avoid token bloat by processing data in scripts, not in agent context.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
