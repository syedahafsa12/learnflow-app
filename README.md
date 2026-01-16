# LearnFlow AI-Powered Python Tutoring Platform

LearnFlow is an AI-powered Python tutoring platform that helps students learn Python programming through conversational AI agents. Students can chat with tutors, write and run code, take quizzes, and track their progress. Teachers can monitor class performance and generate custom exercises.

## Architecture

The LearnFlow platform follows a modern microservices architecture:

```
┌──────────────────────────────────────────────────────────────────┐
│                         KUBERNETES CLUSTER                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ││
│  │  │   Next.js   │    │   FastAPI   │    │   FastAPI   │    ││
│  │  │  Frontend   │    │  Triage Svc │    │ Concepts Svc│    ││
│  │  │ +Monaco Ed  │    │ +Dapr+Agent │    │ +Dapr+Agent │    ││
│  │  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    ││
│  │         │                 │                  │             ││
│  │         └────────────┬────┴──────────────────┘             ││
│  │                      ▼                                      ││
│  │  ┌─────────────────────────────────────────────────────┐   ││
│  │  │                      KAFKA                          │   ││
│  │  │  learning.* | code.* | exercise.* | struggle.*      │   ││
│  │  └─────────────────────────────────────────────────────┘   ││
│  │                      │                                      ││
│  │         └────────────┴────────────┘                        ││
│  │         ▼                         ▼                        ││
│  │  ┌─────────────┐          ┌─────────────┐                  ││
│  │  │ PostgreSQL  │          │   MCP Srv   │                  ││
│  │  │  Neon DB    │          │  (Context)  │                  ││
│  │  └─────────────┘          └─────────────┘                  ││
│  └─────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

## Features

### For Students
- Chat with Python tutor AI agents
- Write and run code in the embedded Monaco editor
- Take coding quizzes and exercises
- Track learning progress

### For Teachers
- Monitor class performance
- Receive struggle alerts when students are stuck
- Generate custom coding exercises

### Python Curriculum
1. Basics: Variables, Data Types, Input/Output, Operators
2. Control Flow: Conditionals, Loops, Break/Continue
3. Data Structures: Lists, Tuples, Dictionaries, Sets
4. Functions: Defining, Parameters, Return Values
5. OOP: Classes, Objects, Inheritance, Encapsulation
6. Files: Reading/Writing, CSV, JSON
7. Errors: Try/Except, Exception Types, Debugging
8. Libraries: Package Management, APIs

## AI Agent System

LearnFlow uses a multi-agent architecture:
- **Triage Agent**: Routes queries to appropriate specialists
- **Concepts Agent**: Explains Python concepts with examples
- **Code Review Agent**: Analyzes code quality and style
- **Debug Agent**: Helps debug errors and provides hints
- **Exercise Agent**: Generates and grades coding challenges
- **Progress Agent**: Tracks mastery and progress

## Technology Stack
- Frontend: Next.js + Monaco Editor
- Backend: FastAPI + OpenAI SDK
- Database: PostgreSQL (Neon)
- Messaging: Apache Kafka on Kubernetes
- Service Mesh: Dapr
- Authentication: Better Auth
- API Gateway: Kong API Gateway
- Container Orchestration: Kubernetes
- Documentation: Docusaurus

## Getting Started

This application is built using AI coding agents and reusable skills. See the skills-library repository for the tools used to build this platform.

## License

MIT
