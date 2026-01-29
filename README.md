# LearnFlow - AI-Powered Python Learning Platform

LearnFlow is an innovative AI-powered Python tutoring platform designed to revolutionize how students learn programming. Featuring a modern, AI-first interface, the platform seamlessly integrates multiple AI agents to provide personalized learning experiences for students and comprehensive insights for teachers.

## 🚀 Key Features

### Student Portal
- **AI Tutor Workspace**: Interactive chat interface with multiple specialized AI agents
- **Code Lab**: Integrated Python code editor with real-time execution and sandboxing
- **Quiz Master**: Adaptive quiz system with immediate feedback and mastery tracking
- **Progress Dashboard**: Visual mastery tracking with detailed analytics and achievement badges
- **Resource Library**: Comprehensive collection of learning materials and tutorials

### Teacher Portal
- **Class Intelligence Dashboard**: Real-time class performance overview with heatmaps
- **Student Deep-Dive**: Detailed individual student progress analysis and timeline views
- **AI Exercise Generator**: Natural language exercise creation with one-click assignment
- **Struggle Detection**: Automatic identification of students needing help with transparent alerts
- **Assignment Management**: Comprehensive assignment creation, tracking, and analytics

### AI Agent System
- **Triage Agent**: Routes queries to appropriate specialists
- **Concepts Agent**: Explains Python concepts with examples and visualizations
- **Code Review Agent**: Analyzes code quality, style (PEP 8), and efficiency
- **Debug Agent**: Helps fix coding errors with guided hints (not full solutions)
- **Exercise Agent**: Generates and auto-grades practice problems
- **Progress Agent**: Tracks and reports learning progress with mastery analytics

## 🎨 Modern UI/UX Design

### Design Philosophy
- **AI-First Interface**: Make AI agent presence and intelligence obvious and engaging
- **Visual Excellence**: Premium, modern aesthetic rivaling top LMS products
- **Intelligent Transparency**: Show users exactly how the system works and why recommendations are made
- **Performance Focused**: Fast, responsive, and optimized for learning flow

### Cool Features
- **Agent Presence UI**: Clear visualization of which AI agent is active with role explanations
- **Struggle Radar**: Subtle real-time indicators when the system detects confusion
- **Mastery Momentum**: Animated progress transitions with celebration effects
- **Explain-My-Mistake Mode**: Focused error explanations without revealing complete solutions
- **Teacher Alert Justification**: Transparent reasoning for all alerts with specific data points

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

## 🛠 Tech Stack

- **Frontend**: Next.js 14+ (App Router), React 18+
- **Styling**: Tailwind CSS with custom design system and CSS modules
- **Editor**: Monaco Editor for professional code editing
- **State Management**: React Context API and client-side state
- **API**: Next.js API routes for AI integration
- **Backend**: FastAPI + OpenAI SDK
- **Database**: PostgreSQL (Neon)
- **Messaging**: Apache Kafka on Kubernetes
- **Service Mesh**: Dapr
- **Authentication**: Better Auth
- **API Gateway**: Kong API Gateway
- **Container Orchestration**: Kubernetes
- **Documentation**: Docusaurus

## 🏁 Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Run Development Server**
   ```bash
   npm run dev
   ```

3. **Open Browser**
   Visit `http://localhost:3000` to access the application

## 📊 Python Curriculum & Mastery System

### Curriculum Modules
1. **Basics**: Variables, Data Types, Input/Output, Operators, Type Conversion
2. **Control Flow**: Conditionals (if/elif/else), For Loops, While Loops, Break/Continue
3. **Data Structures**: Lists, Tuples, Dictionaries, Sets
4. **Functions**: Defining Functions, Parameters, Return Values, Scope
5. **OOP**: Classes & Objects, Attributes & Methods, Inheritance, Encapsulation
6. **Files**: Reading/Writing Files, CSV Processing, JSON Handling
7. **Errors**: Try/Except, Exception Types, Custom Exceptions, Debugging
8. **Libraries**: Installing Packages, Working with APIs, Virtual Environments

### Mastery Calculation
Topic Mastery = weighted average of:
- Exercise completion: 40%
- Quiz scores: 30%
- Code quality ratings: 20%
- Consistency (streak): 10%

### Mastery Levels
- **Beginner** (0-40%): Red
- **Learning** (41-70%): Yellow
- **Proficient** (71-90%): Green
- **Mastered** (91-100%): Blue

## ⚡ Code Execution Sandbox

- Timeout: 5 seconds
- Memory: 50MB
- No file system access (except temporary files)
- No network access
- Allowed imports: standard library only (MVP)

## 🚨 Struggle Detection Triggers

- Same error type 3+ times
- Stuck on exercise > 10 minutes
- Quiz score < 50%
- Student says "I don't understand" or "I'm stuck"
- 5+ failed code executions in a row
- Language analysis indicating frustration or confusion

## 🏆 Hackathon Features

This implementation was designed for hackathon competition with:
- AI-first interface design that exposes intelligence
- Modern, visually impressive UI competitive against top LMS products
- Immediate judge appeal in under 60 seconds
- Comprehensive feature set for both students and teachers
- Cross-platform compatibility and responsive design

## 🤝 Contributing

We welcome contributions to LearnFlow! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
