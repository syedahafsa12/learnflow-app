---
name: agents-md-gen
description: Generate AGENTS.md files to help AI agents understand repository structure and conventions
---

# AGENTS.md Generator

## When to Use
- Creating AGENTS.md for new repositories
- Updating AGENTS.md when project structure changes
- Teaching AI agents about codebase conventions

## Instructions
1. Create/update AGENTS.md in repository root
2. Use `./scripts/generate_agents_md.py` to generate the file
3. Review and customize the generated content as needed

## What is AGENTS.md?
AGENTS.md describes a repository's structure, conventions, and guidelines so AI agents can understand how to work with the codebase effectively.

## Expected Sections
- Repository overview and purpose
- Project structure and directory layout
- Code conventions and standards
- Development workflow
- Testing procedures
- Deployment process
- Key files and their purposes

## Validation
- [ ] AGENTS.md exists in repository root
- [ ] File contains all expected sections
- [ ] Information is accurate and up-to-date

See [REFERENCE.md](./REFERENCE.md) for AGENTS.md best practices.