# MCP Code Execution Pattern Reference

## Purpose
The MCP Code Execution Pattern skill demonstrates how to efficiently integrate Model Context Protocol (MCP) servers with AI agents while minimizing token consumption.

## The Token Problem
Direct MCP integration causes severe token bloat:
- MCP tool definitions consume 10,000+ tokens at startup per server
- Large datasets flow through context multiple times
- A 10,000-row spreadsheet consumes 50,000+ tokens

## The Solution
Wrap MCP calls in code execution scripts:
- SKILL.md defines the capability (~100 tokens)
- Scripts execute MCP calls and process data (0 tokens loaded)
- Only results enter agent context (minimal tokens)

## Features
- Token-efficient MCP integration
- Data filtering and aggregation
- Performance comparison demonstrations
- Best practice patterns

## Usage Patterns
### Basic MCP Client
```bash
python scripts/mcp_client.py
```

### Run Examples
```bash
bash scripts/run_examples.sh
```

### Integration Demo
```bash
python scripts/integration_demo.py
```

## Core Patterns
### 1. Filter Pattern
- Retrieve large dataset via MCP
- Filter data in script
- Return only relevant subset to context

### 2. Aggregate Pattern  
- Retrieve data via MCP
- Calculate statistics in script
- Return only summary to context

### 3. Process Pattern
- Retrieve raw data via MCP
- Transform in script
- Return only processed results to context

## Configuration Options
- Customize MCP server URL
- Modify filtering criteria
- Adjust aggregation methods
- Extend client functionality

## LearnFlow Applications
- Student progress analytics
- Exercise performance insights
- Error pattern detection
- Code quality metrics

## Dependencies
- Python 3.7+
- Requests library
- MCP server (for real implementations)

## Best Practices
- Always process data in scripts, not in agent context
- Return minimal, relevant information
- Use aggregation for large datasets
- Implement proper error handling
- Document token savings achieved

## Integration with AI Agents
- Claude Code can use efficient MCP patterns
- Goose can leverage token-saving integrations
- Achieves 80-98% token reduction while maintaining capabilities
