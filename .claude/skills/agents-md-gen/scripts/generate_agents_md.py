#!/usr/bin/env python3
"""
AGENTS.md Generator Script
This script analyzes a repository and generates an AGENTS.md file to help AI agents understand the codebase.
"""

import os
import sys
import subprocess
from pathlib import Path

def get_repo_structure(start_path):
    """Get the directory structure of the repository."""
    structure = []
    for root, dirs, files in os.walk(start_path, topdown=True):
        # Skip certain directories that shouldn't be in AGENTS.md
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]

        level = root.replace(start_path, '').count(os.sep)
        indent = '    ' * level
        structure.append(f'{indent}{os.path.basename(root)}/')
        subindent = '    ' * (level + 1)
        for file in files:
            if not file.startswith('.'):
                structure.append(f'{subindent}{file}')

    return '\n'.join(structure)

def get_git_info():
    """Get basic git information about the repository."""
    try:
        # Get repository name from git remote
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'],
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            repo_url = result.stdout.strip()
            return repo_url.split('/')[-1].replace('.git', '')
        else:
            return "Unknown Repository"
    except:
        return "Unknown Repository"

def generate_agents_md():
    """Generate the AGENTS.md content."""
    repo_name = get_git_info()

    content = f"""# AGENTS.md - {repo_name}

## Repository Overview
This repository contains the {repo_name} project. The purpose of this codebase is to provide a well-structured application that can be understood and modified by AI agents.

## Directory Structure
```
{get_repo_structure('.')}
```

## Technology Stack
The project utilizes the following technologies:
- Language: [Specify languages used in the project]
- Frameworks: [Specify frameworks used]
- Dependencies: [List key dependencies]

## Key Files and Directories
- `README.md`: Project overview and setup instructions
- `package.json`/`requirements.txt`/`Cargo.toml`: Dependency management
- Main application files: [Specify main entry points]

## Code Conventions
- Follow standard conventions for the primary language used
- Maintain consistent naming patterns
- Document public functions and classes

## Development Workflow
- Make changes in feature branches
- Write tests for new functionality
- Follow the existing code style

## Testing Strategy
- Unit tests: [Location of unit tests]
- Integration tests: [Location of integration tests]
- Test execution: [Command to run tests]

## Deployment Process
- Build steps: [Commands to build the project]
- Deployment targets: [Where and how to deploy]

## Special Instructions for AI Agents
- When modifying code, maintain backward compatibility where possible
- Follow the existing patterns and conventions
- Add documentation for new functions and classes
- Consider the impact on related components when making changes
"""

    return content

def main():
    """Main function to generate AGENTS.md file."""
    try:
        agents_content = generate_agents_md()

        # Write to AGENTS.md in the current directory
        with open('AGENTS.md', 'w', encoding='utf-8') as f:
            f.write(agents_content)

        print("✓ AGENTS.md generated successfully!")
        print("File saved as AGENTS.md in the current directory.")

    except Exception as e:
        print(f"✗ Error generating AGENTS.md: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()