---
name: mcp-code-execution
description: MCP with efficient code execution pattern to reduce token usage
---

# MCP Code Execution Pattern

## When to Use
- Connecting MCP servers to AI agents efficiently
- Reducing token consumption from tool definitions
- Wrapping MCP calls in scripts for minimal context flow
- Implementing token-efficient agent interactions

## Instructions
1. Use scripts to execute MCP interactions: `./scripts/mcp_client.py`
2. Process data filtering in scripts, not in context
3. Return minimal results to agent context
4. Follow code execution pattern to reduce tokens by 80-98%

## The Problem
Direct MCP connections consume 41%+ of context before conversation starts:
- Tool definitions: 50k+ tokens loaded at startup
- Intermediate results: Additional 50k+ tokens
- Total before conversation: 100k+ tokens consumed

## The Solution
Wrap MCP functionality in scripts that execute outside context:
- SKILL.md: ~100 tokens loaded when triggered
- Scripts: Execute with full MCP access (0 tokens in context)
- Results: Only minimal output enters context

## Validation
- [ ] Scripts execute MCP calls successfully
- [ ] Token usage reduced significantly
- [ ] Full functionality maintained
- [ ] Results are minimal and focused

See [REFERENCE.md](./REFERENCE.md) for implementation patterns and examples.