# MCP Code Execution Pattern - Reference Documentation

## Overview
The MCP Code Execution pattern is a design approach that wraps Model Context Protocol (MCP) server functionality in executable scripts to dramatically reduce token consumption while maintaining full functionality.

## The Token Problem

### Direct MCP Approach (Inefficient)
When connecting MCP servers directly to AI agents:

```
Context Window Before Conversation: 100,000+ tokens
├── MCP Tool Definitions: 50,000+ tokens
├── Intermediate Results: 50,000+ tokens
└── Available for Conversation: < 5%
```

**Problems:**
- Tool definitions load at startup (50k+ tokens)
- Every intermediate result flows through context twice
- Rapidly consumes context window before real work begins

### MCP Code Execution Pattern (Efficient)
Wrap MCP functionality in scripts that execute outside the context window:

```
Context Window Before Conversation: 100,000+ tokens
├── SKILL.md: ~100 tokens (when triggered)
├── Scripts: 0 tokens (execute outside context)
├── MCP Calls: 0 tokens (made by scripts)
└── Available for Conversation: > 99%
```

## Pattern Implementation

### 1. SKILL.md Structure
Keep instructions minimal (~100 tokens):

```markdown
---
name: example-mcp-skill
description: Example MCP skill with code execution
---
# Example Skill

## When to Use
- When you need to interact with external systems
- To reduce token usage from MCP calls

## Instructions
Run: `./scripts/example_script.py`

## Validation
- [ ] Script executes successfully
- [ ] Minimal output returned
```

### 2. Script Structure
Scripts perform the actual work with MCP access:

```python
#!/usr/bin/env python3
# scripts/example_script.py

# Execute MCP calls within the script
# Process/filter data within the script
# Return minimal results to context

result = mcp_call(...)  # MCP call happens in script
filtered_result = process_data(result)  # Processing happens in script
print(filtered_result)  # Only minimal output to context
```

### 3. Token Efficiency Gains
- **Before**: 50,000+ tokens for MCP tool definitions
- **After**: ~100 tokens for skill instructions
- **Savings**: 98%+ reduction in token usage
- **Benefit**: More room for actual work in context

## Best Practices

### 1. Data Filtering
Perform data filtering in scripts, not in context:

```python
# ❌ Inefficient - brings all data to context
all_data = mcp_get_large_dataset()
filtered_data = [item for item in all_data if item.status == 'active']
return filtered_data  # Still sends filtered data to context

# ✅ Efficient - filter in script
all_data = mcp_get_large_dataset()
filtered_data = [item for item in all_data if item.status == 'active']
summary = f"Found {len(filtered_data)} active items"  # Minimal output
print(summary)  # Only summary to context
```

### 2. Result Summarization
Return summaries instead of full datasets:

```python
# ❌ Sends lots of data to context
def get_cluster_status():
    pods = kubectl_get_pods()
    return pods  # Large JSON structure

# ✅ Sends minimal data to context
def get_cluster_status():
    pods = kubectl_get_pods()
    running = sum(1 for p in pods if p.status.phase == 'Running')
    total = len(pods)
    print(f"{running}/{total} pods running")
```

### 3. Error Handling
Handle errors gracefully in scripts:

```python
try:
    result = mcp_call()
    print("Success")
except Exception as e:
    print(f"Error: {str(e)[:100]}...")  # Limited error output
    exit(1)
```

## Examples

### Kubernetes Operations
```bash
# Instead of loading all kubectl commands as MCP tools
# Use script that executes kubectl and returns minimal output

./scripts/mcp_client.py --system kubernetes --operation get --resource-type pods --namespace default
# Output: "Found 3 pods in namespace default: 2 Running, 1 Pending"
```

### Database Queries
```bash
# Instead of loading full database schema as MCP tools
# Use script that executes query and returns summary

./scripts/mcp_client.py --system postgresql --operation execute_query --query "SELECT COUNT(*) FROM users;"
# Output: "Query executed successfully, returning 1 rows: 1245"
```

### Message Queue Operations
```bash
# Instead of loading all Kafka commands as MCP tools
# Use script that executes Kafka CLI and returns summary

./scripts/mcp_client.py --system kafka --operation list_topics
# Output: "Found 5 Kafka topics: users, orders, logs, alerts, metrics"
```

## Security Considerations
- Validate inputs to scripts
- Implement proper authentication
- Use parameterized queries to prevent injection
- Limit script permissions appropriately

## Performance Benefits
- **Token Reduction**: 80-98% decrease in context usage
- **Response Time**: Faster startup (no tool loading delay)
- **Scalability**: Can handle more MCP integrations
- **Maintainability**: Scripts can be version controlled separately

## Troubleshooting
- If scripts fail, check permissions and dependencies
- Monitor script execution logs for debugging
- Verify MCP server connectivity from script context
- Test scripts independently before integrating with skills

## Integration with LearnFlow
For the LearnFlow platform, MCP Code Execution enables:
- Efficient monitoring of microservices
- Token-saving database operations
- Streamlined Kafka topic management
- Reduced overhead for AI agent context management