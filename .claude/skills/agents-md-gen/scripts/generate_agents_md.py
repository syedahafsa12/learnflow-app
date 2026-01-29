#!/usr/bin/env python3
"""
AGENTS.md Generator
Analyzes repository structure and creates AGENTS.md file for AI agents
"""

import os
import sys
import json
from pathlib import Path

def analyze_repo_structure(root_path="."):
    """Analyze repository structure and return organized information."""
    structure = {
        "root_files": [],
        "directories": {},
        "important_configs": []
    }

    root = Path(root_path)

    # Walk through the directory
    for item in root.rglob("*"):
        if item.is_file():
            rel_path = str(item.relative_to(root))

            # Skip certain files/directories
            skip_patterns = ['.git', '__pycache__', '.pyc', 'node_modules', '.venv', 'venv']
            if any(skip in rel_path for skip in skip_patterns):
                continue

            # Categorize files
            if item.name in ['package.json', 'requirements.txt', 'Dockerfile', 'docker-compose.yml',
                            'README.md', 'CLAUDE.md', '.gitignore', 'skaffold.yaml', 'kustomization.yaml']:
                structure["important_configs"].append(rel_path)
            elif '/' not in rel_path:  # Root level files
                structure["root_files"].append(rel_path)
            else:  # Files in subdirectories
                dir_path = '/'.join(rel_path.split('/')[:-1])
                if dir_path not in structure["directories"]:
                    structure["directories"][dir_path] = []
                structure["directories"][dir_path].append(item.name)

    return structure

def generate_agents_md(structure):
    """Generate AGENTS.md content based on repository structure."""
    content = "# AGENTS.md\n"
    content += "Repository structure and guidelines for AI agents\n\n"

    content += "## Root Files\n"
    for file in structure["root_files"]:
        content += f"- `{file}`\n"
    content += "\n"

    content += "## Configuration Files\n"
    for config in structure["important_configs"]:
        content += f"- `{config}` - Important configuration file\n"
    content += "\n"

    content += "## Directory Structure\n"
    for directory, files in structure["directories"].items():
        content += f"### {directory}/\n"
        for file in files:
            content += f"- `{file}`\n"
        content += "\n"

    content += "## File Extensions and Technologies\n"
    content += "Common file extensions and their purposes in this repository:\n"
    content += "- `.py`: Python source code\n"
    content += "- `.js`, `.jsx`: JavaScript/JSX code\n"
    content += "- `.ts`, `.tsx`: TypeScript/TSX code\n"
    content += "- `.md`: Documentation files\n"
    content += "- `.yaml`, `.yml`: Configuration files\n"
    content += "- `.json`: Data and configuration files\n"
    content += "- `.sh`: Shell scripts\n"
    content += "- `.sql`: Database scripts\n\n"

    content += "## Guidelines for AI Agents\n"
    content += "1. Respect the existing code style and patterns\n"
    content += "2. Follow the established architecture and design principles\n"
    content += "3. Maintain backward compatibility when possible\n"
    content += "4. Update documentation when making changes\n"
    content += "5. Consider the impact on related components\n"

    return content

def main():
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = "."

    print(f"Analyzing repository structure in {repo_path}...")
    structure = analyze_repo_structure(repo_path)

    print("Generating AGENTS.md...")
    agents_md_content = generate_agents_md(structure)

    # Write to file
    with open('AGENTS.md', 'w') as f:
        f.write(agents_md_content)

    print("✓ AGENTS.md generated successfully!")

if __name__ == "__main__":
    main()
