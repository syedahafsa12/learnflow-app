# AGENTS.md - LearnFlow AI-Powered Python Tutoring Platform

## Repository Overview

LearnFlow is an AI-powered Python tutoring platform built using skills-based AI agent development. The platform enables students to learn Python programming through conversational AI agents, write and execute code, take quizzes, and track their progress. Teachers can monitor class performance and generate custom exercises.

This repository demonstrates the **MCP Code Execution Pattern** where AI agents (Claude Code, Goose) autonomously built the entire application using reusable skills.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    KUBERNETES CLUSTER (Minikube)                │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    LEARNFLOW NAMESPACE                     │ │
│  │                                                             │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │  │  Triage      │  │  Concepts    │  │ Code Review  │    │ │
│  │  │  Agent       │  │  Agent       │  │ Agent        │    │ │
│  │  │  + Dapr      │  │  + Dapr      │  │ + Dapr       │    │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │ │
│  │         │                  │                  │            │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │  │  Debug       │  │  Exercise    │  │  Progress    │    │ │
│  │  │  Agent       │  │  Agent       │  │  Agent       │    │ │
│  │  │  + Dapr      │  │  + Dapr      │  │  + Dapr      │    │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │ │
│  │         │                  │                  │            │ │
│  │         └──────────────────┴──────────────────┘            │ │
│  │                            ▼                                │ │
│  │                  ┌────────────────────┐                    │ │
│  │                  │  Next.js Frontend  │                    │ │
│  │                  │  + Monaco Editor   │                    │ │
│  │                  └─────────┬──────────┘                    │ │
│  └────────────────────────────┼─────────────────────────────────┘ │
│                                ▼                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    KAFKA NAMESPACE                         │ │
│  │  ┌───────────────────────────────────────────────────┐    │ │
│  │  │            Apache Kafka (Strimzi)                 │    │ │
│  │  │  Topics:                                          │    │ │
│  │  │  - learning.query    - learning.response          │    │ │
│  │  │  - learning.progress - learning.struggle          │    │ │
│  │  │  - code.execution    - code.review                │    │ │
│  │  │  - exercise.generated - exercise.attempt          │    │ │
│  │  └───────────────────────────────────────────────────┘    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                ▼                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   TASKFLOW NAMESPACE                       │ │
│  │  ┌───────────────────────────────────────┐                │ │
│  │  │      PostgreSQL Database              │                │ │
│  │  │      Database: learnflow              │                │ │
│  │  │      - users, students, teachers      │                │ │
│  │  │      - modules, progress              │                │ │
│  │  │      - conversations, code_submissions│                │ │
│  │  │      - exercises, quizzes             │                │ │
│  │  └───────────────────────────────────────┘                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    DAPR-SYSTEM NAMESPACE                   │ │
│  │  - dapr-operator, dapr-sentry, dapr-placement              │ │
│  │  - dapr-sidecar-injector, dapr-dashboard                   │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
learnflow-app/
├── .claude/
│   └── skills/              # Reusable AI agent skills
│       ├── agents-md-gen/   # Generate AGENTS.md files
│       ├── kafka-k8s-setup/ # Deploy Kafka infrastructure
│       ├── postgres-k8s-setup/ # Deploy PostgreSQL
│       ├── fastapi-dapr-agent/ # Create microservices
│       ├── mcp-code-execution/ # MCP pattern examples
│       ├── nextjs-k8s-deploy/ # Deploy Next.js apps
│       └── docusaurus-deploy/ # Deploy documentation
├── backend/
│   ├── triage-agent/        # Routes student queries to specialists
│   │   ├── main.py          # FastAPI application
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── concepts-agent/      # Explains Python concepts
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── code-review-agent/   # Analyzes code quality
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── debug-agent/         # Helps debug errors
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── exercise-agent/      # Generates coding challenges
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── progress-agent/      # Tracks learning progress
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── schema.sql           # PostgreSQL database schema
├── frontend/
│   ├── pages/               # Next.js pages
│   │   ├── index.js         # Main dashboard
│   │   ├── _app.js          # App configuration
│   │   └── api/
│   │       └── tutor.js     # API endpoints
│   ├── components/          # React components
│   ├── styles/              # CSS styles
│   ├── package.json
│   ├── Dockerfile
│   └── next.config.js
├── k8s/
│   ├── learnflow-namespace.yaml
│   ├── triage-agent.yaml
│   ├── concepts-agent.yaml
│   ├── code-review-agent.yaml
│   ├── remaining-agents.yaml
│   └── kafka-topics.yaml
├── AGENTS.md               # This file
└── README.md               # Project overview
```

## Technology Stack

### Infrastructure Layer
- **Kubernetes**: Container orchestration (Minikube for local development)
- **Dapr**: Distributed application runtime for microservices (state management, pub/sub)
- **Apache Kafka**: Event streaming platform (Strimzi operator)
- **PostgreSQL**: Relational database for persistent storage

### Backend Services
- **FastAPI**: Modern Python web framework for building APIs
- **Python 3.11**: Primary programming language
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for FastAPI applications

### Frontend
- **Next.js 14**: React framework with App Router
- **React 18**: JavaScript library for building user interfaces
- **Monaco Editor**: Code editor component (same engine as VS Code)
- **TypeScript**: Type-safe JavaScript

### AI & Agent Development
- **Claude Code**: Anthropic's agentic CLI tool
- **Goose**: Open-source AI agent from AAIF
- **Skills**: Reusable instructions for AI agents following MCP Code Execution pattern

## AI Agent System

### Backend Microservices (AI Tutoring Agents)

#### 1. Triage Agent (`triage-agent`)
**Purpose**: Routes student queries to appropriate specialist agents

**Key Functionality**:
- Analyzes query content and context
- Determines routing based on keywords and patterns
- Returns routing decision with confidence score

**API Endpoints**:
- `GET /health` - Health check
- `POST /triage` - Analyze and route student query

**Routing Logic**:
```python
Concept queries → concepts-agent
Error/debug queries → debug-agent
Code review requests → code-review-agent
Exercise requests → exercise-agent
Progress queries → progress-agent
```

**Location**: `backend/triage-agent/main.py`

#### 2. Concepts Agent (`concepts-agent`)
**Purpose**: Explains Python programming concepts with examples

**Key Functionality**:
- Provides concept explanations adapted to student level
- Generates code examples
- Creates visual analogies

**Topics Covered**:
- Basics (variables, data types, operators)
- Control flow (conditionals, loops)
- Data structures (lists, tuples, dictionaries, sets)
- Functions, OOP, file handling, error handling

**Location**: `backend/concepts-agent/main.py`

#### 3. Code Review Agent (`code-review-agent`)
**Purpose**: Analyzes student code for quality, style, and correctness

**Key Functionality**:
- PEP 8 style compliance checking
- Code quality assessment
- Performance optimization suggestions
- Readability improvements

**Location**: `backend/code-review-agent/main.py`

#### 4. Debug Agent (`debug-agent`)
**Purpose**: Helps students debug errors and fix code issues

**Key Functionality**:
- Parses error messages
- Identifies root causes
- Provides hints before solutions
- Explains common Python errors

**Location**: `backend/debug-agent/main.py`

#### 5. Exercise Agent (`exercise-agent`)
**Purpose**: Generates and auto-grades coding challenges

**Key Functionality**:
- Creates exercises based on difficulty level
- Generates test cases
- Auto-grades submissions
- Provides feedback

**Location**: `backend/exercise-agent/main.py`

#### 6. Progress Agent (`progress-agent`)
**Purpose**: Tracks student mastery and learning progress

**Key Functionality**:
- Calculates mastery scores by module
- Tracks completion rates
- Identifies learning patterns
- Generates progress reports

**Mastery Calculation**:
```
Topic Mastery = weighted average of:
- Exercise completion: 40%
- Quiz scores: 30%
- Code quality ratings: 20%
- Consistency (streak): 10%
```

**Location**: `backend/progress-agent/main.py`

## Database Schema

### Core Tables

**users** - User authentication and basic info
- Columns: id, email, username, password_hash, role, full_name, created_at, last_login

**students** - Student profiles (extends users)
- Columns: id, user_id, current_module, total_mastery_score, learning_streak_days, last_activity

**teachers** - Teacher profiles (extends users)
- Columns: id, user_id, department, specialization

**modules** - Python curriculum (8 modules)
- Columns: id, name, description, order_index, topics

**student_progress** - Progress tracking by module
- Columns: id, student_id, module_id, mastery_score, exercises_completed, quiz_score, code_quality_avg, last_updated

**conversations** - Chat history between students and AI agents
- Columns: id, student_id, agent_name, query, response, routed_to, confidence, created_at

**code_submissions** - Student code submissions with execution results
- Columns: id, student_id, module_id, code, output, error_message, execution_time_ms, quality_score, feedback, submitted_at

**exercises** - Coding challenges
- Columns: id, module_id, title, description, difficulty, starter_code, test_cases, solution, created_by, created_at

**exercise_attempts** - Student attempts at exercises
- Columns: id, student_id, exercise_id, code, passed, test_results, attempts_count, time_spent_seconds, submitted_at

**quizzes** - Module quizzes
- Columns: id, module_id, title, questions (JSONB), passing_score, created_at

**quiz_attempts** - Student quiz attempts
- Columns: id, student_id, quiz_id, answers (JSONB), score, passed, completed_at

**struggle_alerts** - Alerts for students needing help
- Columns: id, student_id, module_id, trigger_type, description, severity, resolved, resolved_by, created_at, resolved_at

**Schema Location**: `backend/schema.sql`

## Event-Driven Architecture (Kafka Topics)

### Learning Events
- **learning.query**: Student asks question → Triage agent routes
- **learning.response**: Agent responds → Stored in conversations table
- **learning.progress**: Progress update → Progress agent calculates mastery
- **learning.struggle**: Student struggling → Teacher alert generated

### Code Events
- **code.execution**: Code submitted → Executed in sandbox
- **code.review**: Review requested → Code review agent analyzes

### Exercise Events
- **exercise.generated**: New exercise created → Assigned to students
- **exercise.attempt**: Student attempts exercise → Auto-graded

## Development Workflow

### How This Application Was Built

This application was built using **skills-based AI agent development** with the MCP Code Execution pattern:

1. **Skills Created** (in `skills-library` repository):
   - Each skill has ~100 token SKILL.md + executable scripts
   - Scripts execute outside agent context (0 tokens)
   - Only results return to agent (~10-20 tokens)

2. **Infrastructure Deployed via Skills**:
   ```
   AI Prompt: "Deploy Kafka for event streaming"
   → kafka-k8s-setup skill loads
   → Scripts deploy Strimzi operator + Kafka cluster
   → Returns: "✓ Kafka deployed with 3 brokers"
   ```

3. **Microservices Created via Skills**:
   ```
   AI Prompt: "Create triage-agent microservice with Dapr"
   → fastapi-dapr-agent skill loads
   → Generates FastAPI code + Dockerfile + K8s manifests
   → Deploys to cluster with Dapr sidecar
   → Returns: "✓ triage-agent deployed and healthy"
   ```

4. **Total Token Usage**:
   - Traditional approach: ~100,000 tokens
   - Skills approach: ~1,300 tokens
   - **Efficiency: 98.7% reduction**

### For AI Agents Working on This Codebase

When modifying or extending LearnFlow:

1. **Use existing skills** in `.claude/skills/` directory
2. **For new infrastructure**: Use kafka-k8s-setup, postgres-k8s-setup skills
3. **For new microservices**: Use fastapi-dapr-agent skill
4. **For frontend changes**: Use nextjs-k8s-deploy skill
5. **For documentation**: Use docusaurus-deploy skill

### Code Conventions

- **Python**: Follow PEP 8 style guide
- **FastAPI**: Use Pydantic models for request/response validation
- **Async/Await**: Prefer async functions for I/O operations
- **Type Hints**: Always include type annotations
- **Error Handling**: Use try/except with specific exception types
- **Logging**: Use Python logging module, not print statements
- **Environment Variables**: Use for configuration (DATABASE_URL, KAFKA_BOOTSTRAP_SERVERS)

### Testing Strategy

**Unit Tests**:
- Location: `backend/{service}/tests/`
- Framework: pytest
- Coverage: Aim for >80%

**Integration Tests**:
- Test Kafka pub/sub between services
- Test database operations
- Test Dapr state management

**End-to-End Tests**:
- Student journey: Login → Ask question → Get response → Track progress
- Teacher journey: View alerts → Generate exercise → Assign to class

**Test Execution**:
```bash
# Run all tests
pytest backend/

# Run specific service tests
pytest backend/triage-agent/tests/

# Run with coverage
pytest --cov=backend --cov-report=html
```

## Deployment

### Local Development (Minikube)

```bash
# Start Minikube cluster
minikube start --cpus=4 --memory=8192 --driver=docker

# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n learnflow
kubectl get pods -n kafka
kubectl get pods -n taskflow
kubectl get pods -n dapr-system

# Port forward to access services
kubectl port-forward -n learnflow svc/triage-agent 8000:8000
kubectl port-forward -n learnflow svc/frontend 3000:3000
```

### Production Deployment

For production, deploy to cloud Kubernetes:
- **Azure**: Azure Kubernetes Service (AKS)
- **Google Cloud**: Google Kubernetes Engine (GKE)
- **AWS**: Elastic Kubernetes Service (EKS)
- **Oracle**: Oracle Container Engine for Kubernetes (OKE)

Use GitOps with Argo CD for continuous deployment.

## Monitoring & Observability

### Dapr Dashboard
```bash
minikube service dapr-dashboard -n dapr-system
```

### Logs
```bash
# View service logs
kubectl logs -n learnflow deployment/triage-agent -c triage-agent

# View Dapr sidecar logs
kubectl logs -n learnflow deployment/triage-agent -c daprd

# Stream logs
kubectl logs -n learnflow deployment/triage-agent -c triage-agent -f
```

### Metrics
- Prometheus + Grafana (to be deployed via prometheus-grafana-setup skill)
- Service mesh metrics via Dapr

## API Documentation

Each microservice exposes OpenAPI documentation:

```
http://{service-url}:8000/docs     # Swagger UI
http://{service-url}:8000/redoc    # ReDoc
http://{service-url}:8000/openapi.json  # OpenAPI schema
```

## Environment Variables

### Backend Services
- `DATABASE_URL`: PostgreSQL connection string
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers
- `SERVICE_NAME`: Service identifier for logging
- `DAPR_HTTP_PORT`: Dapr HTTP port (default: 3500)
- `DAPR_GRPC_PORT`: Dapr gRPC port (default: 50001)

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API base URL
- `NEXT_PUBLIC_WS_URL`: WebSocket URL for real-time updates

## Special Instructions for AI Agents

### When Adding New Features

1. **New Microservice**: Use `fastapi-dapr-agent` skill
2. **New Database Tables**: Update `backend/schema.sql` and apply migrations
3. **New Kafka Topics**: Update `k8s/kafka-topics.yaml`
4. **New Frontend Pages**: Follow Next.js 14 App Router conventions
5. **Update This File**: Keep AGENTS.md in sync with changes

### When Debugging

1. Check pod status: `kubectl get pods -n learnflow`
2. View logs: `kubectl logs -n learnflow deployment/{service}`
3. Check Dapr status: `kubectl get pods -n dapr-system`
4. Test service health: `curl http://{service}:8000/health`

### When Refactoring

- Maintain backward compatibility for API endpoints
- Update OpenAPI documentation
- Run full test suite before committing
- Update AGENTS.md with architectural changes

## Python Curriculum (8 Modules)

1. **Module 1: Basics** - Variables, Data Types, Input/Output, Operators, Type Conversion
2. **Module 2: Control Flow** - Conditionals, For Loops, While Loops, Break, Continue
3. **Module 3: Data Structures** - Lists, Tuples, Dictionaries, Sets
4. **Module 4: Functions** - Defining Functions, Parameters, Return Values, Scope
5. **Module 5: OOP** - Classes, Objects, Attributes, Methods, Inheritance, Encapsulation
6. **Module 6: Files** - Reading/Writing Files, CSV Processing, JSON Handling
7. **Module 7: Errors** - Try/Except, Exception Types, Custom Exceptions, Debugging
8. **Module 8: Libraries** - Installing Packages, Working with APIs, Virtual Environments

## License

MIT

---

**Built with AI Agents for Hackathon III: Reusable Intelligence and Cloud-Native Mastery**

This repository demonstrates how AI coding agents can autonomously build complex, production-ready applications using reusable skills and the MCP Code Execution pattern.
