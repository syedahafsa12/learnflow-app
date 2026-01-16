# AGENTS.md Reference Guide

## Purpose
AGENTS.md files help AI agents understand repository structures, conventions, and guidelines so they can work effectively with the codebase.

## Format Specifications

### Required Sections
1. **Repository Overview**
   - Brief description of the project
   - Main purpose and functionality
   - Target audience/users

2. **Directory Structure**
   ```
   .
   ├── src/          # Source code files
   ├── tests/        # Unit and integration tests
   ├── docs/         # Documentation files
   └── config/       # Configuration files
   ```

3. **Technology Stack**
   - Languages used (JavaScript, Python, etc.)
   - Frameworks (React, Express, Django, etc.)
   - Build tools (Webpack, Maven, etc.)
   - Testing frameworks (Jest, Pytest, etc.)

4. **Entry Points**
   - Main application files
   - API endpoints
   - Configuration entry points

5. **Conventions**
   - Coding standards
   - Naming conventions
   - File organization patterns
   - Branch naming conventions

6. **Special Instructions**
   - Environment setup
   - Secret management
   - Deployment procedures
   - Common pitfalls

## Best Practices
- Keep descriptions concise but informative
- Use code blocks for directory structures
- Include file extensions when relevant
- Mention dependencies and setup requirements
- Highlight important configuration files
- Point out any unusual architectural decisions

## Example Template
```markdown
# Project Name AGENTS.md

## Overview
This project does X and serves Y users. It's built with Z technologies.

## Directory Structure
```
.
├── src/              # Source code
│   ├── components/   # React components
│   └── utils/        # Utility functions
├── tests/            # Test files
├── public/           # Static assets
└── config/           # Configuration
```

## Technologies
- Language: JavaScript (ES6+)
- Framework: React 18
- State Management: Redux Toolkit
- Styling: Tailwind CSS
- Testing: Jest + React Testing Library

## Entry Points
- `src/index.js`: Main application entry point
- `src/App.js`: Root component
- `public/index.html`: HTML template

## Conventions
- Component files use PascalCase
- Utility functions use camelCase
- Tests are co-located with source files

## Special Instructions
- Run with `npm start`
- Secrets stored in `.env.local`
- Tests run with `npm test`
```