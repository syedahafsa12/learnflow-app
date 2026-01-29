---
name: mcp-code-execution
description: MCP with code execution pattern for efficient context management
---

# MCP Code Execution Pattern

## When to Use
- User asks to interact with external data sources via MCP
- Need to reduce token consumption with large datasets
- Want to wrap MCP calls in efficient code execution
- Building AI agents that access external systems

## Instructions
1. Create MCP client: `python scripts/mcp_client.py`
2. Run examples: `bash scripts/run_examples.sh`
3. Test efficiency: Compare direct MCP vs code execution pattern
4. Verify token reduction achieved

## Validation
- [ ] MCP client connects successfully
- [ ] Code execution reduces token usage
- [ ] Examples run without errors

See [REFERENCE.md](./REFERENCE.md) for pattern explanation and best practices.
