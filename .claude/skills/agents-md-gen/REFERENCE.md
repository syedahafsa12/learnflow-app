# AGENTS.md Generator Reference

## Purpose
The AGENTS.md Generator skill creates comprehensive documentation files that help AI agents understand repository structure, file purposes, and development guidelines.

## Features
- Automatically analyzes directory structure
- Identifies important configuration files
- Categorizes files by type and location
- Generates standardized documentation format

## Usage Patterns
### Basic Usage
```bash
python scripts/generate_agents_md.py
```

### Target Specific Directory
```bash
python scripts/generate_agents_md.py /path/to/repo
```

## Customization Options
- Modify the `skip_patterns` in the script to exclude different file types
- Adjust the `important_configs` detection to recognize project-specific files
- Customize the guidelines section based on project requirements

## Output Format
The generated AGENTS.md includes:
- Root-level file listing
- Configuration file identification
- Directory structure breakdown
- File extension descriptions
- Development guidelines for AI agents

## Best Practices
- Run this script when starting new projects
- Regenerate when major structural changes occur
- Review and customize the output for project-specific needs
- Include in initial project setup documentation

## Integration with AI Agents
- Claude Code can use this to understand project structure
- Goose can leverage this for guided development
- Other AI agents can use this as a reference for repository navigation
