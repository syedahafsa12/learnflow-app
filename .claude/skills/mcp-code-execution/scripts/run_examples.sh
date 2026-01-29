#!/bin/bash

# MCP Code Execution Pattern Examples
# Demonstrates efficient token usage with MCP integration

set -e  # Exit on any error

echo "MCP Code Execution Pattern Examples"
echo "===================================="

echo ""
echo "Example 1: Comparing Direct MCP vs Code Execution Pattern"
echo "--------------------------------------------------------"

echo "Direct MCP approach (inefficient - would return 10,000 rows to context):"
echo "  TOOL CALL: mcp.getData(datasetId: 'large-student-data')"
echo "  → Returns 10,000 rows of data directly to agent context"
echo "  → Consumes ~50,000 tokens"
echo ""

echo "Code Execution approach (efficient):"
echo "  Agent executes script that calls MCP internally"
echo "  Script processes data and returns only summary:"
python scripts/mcp_client.py

echo ""
echo "Example 2: Real-world scenario"
echo "------------------------------"
echo "Scenario: Get struggling students from large dataset"
echo ""
echo "Direct MCP (token inefficient):"
echo "  Agent gets full student data (10k records) and processes in context"
echo "  Result: Massive context bloat"
echo ""
echo "Code Execution (token efficient):"
echo "  Agent runs script that:"
echo "    1. Calls MCP to get student data"
echo "    2. Filters for struggling students (internal processing)"
echo "    3. Returns only 50 struggling students to context"
echo "  Result: Only ~500 tokens used"

echo ""
echo "Example 3: Performance Comparison"
echo "---------------------------------"
echo "Direct MCP: 50,000+ tokens for 10k rows"
echo "Code Execution: ~500 tokens for filtered results"
echo "Token Savings: ~99% reduction!"

echo ""
echo "✓ MCP Code Execution Pattern examples completed!"
echo "This demonstrates how to achieve 80-98% token reduction while maintaining full capability."
