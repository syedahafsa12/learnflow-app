# LearnFlow - AI-Powered Python Learning Platform

LearnFlow is an innovative AI-powered Python tutoring platform designed to revolutionize how students learn programming. Built with Next.js, the platform features an intuitive interface that seamlessly integrates multiple AI agents to provide personalized learning experiences.

## 🚀 Features

### Student Portal
- **AI Tutor Workspace**: Interactive chat interface with multiple specialized AI agents
- **Code Lab**: Integrated Python code editor with real-time execution
- **Quiz Master**: Adaptive quiz system with immediate feedback
- **Progress Tracking**: Visual mastery tracking with detailed analytics
- **Resource Library**: Comprehensive collection of learning materials

### Teacher Portal
- **Class Intelligence Dashboard**: Real-time class performance overview
- **Student Deep-Dive**: Detailed individual student progress analysis
- **AI Exercise Generator**: Natural language exercise creation
- **Struggle Detection**: Automatic identification of students needing help

### AI Agent System
- **Triage Agent**: Routes queries to appropriate specialists
- **Concepts Agent**: Explains Python concepts with examples
- **Code Review Agent**: Analyzes code quality and style
- **Debug Agent**: Helps fix coding errors
- **Exercise Agent**: Generates practice problems
- **Progress Agent**: Tracks and reports learning progress

## 🎨 Design Highlights

### Modern UI/UX
- Clean, minimalist interface focused on learning
- Responsive design for all device sizes
- Dark/light mode support
- Accessibility-first approach

### Cool Features
- **Agent Presence UI**: Clear visualization of which AI agent is active
- **Struggle Radar**: Subtle real-time indicators when confusion is detected
- **Mastery Momentum**: Animated progress transitions with celebration effects
- **Explain-My-Mistake Mode**: Focused error explanations without full solutions
- **Teacher Alert Justification**: Transparent reasoning for all alerts

## 🛠 Tech Stack

- **Frontend**: Next.js 14+, React 18+
- **Styling**: Tailwind CSS with custom design system
- **Editor**: Monaco Editor for code editing
- **State Management**: React Context API
- **API**: Next.js API routes for AI integration

## 📁 Project Structure

```
frontend/
├── components/           # Reusable UI components
│   ├── ui/              # Base UI components (Button, Card, etc.)
│   └── Layout.jsx       # Main application layout
├── pages/               # Application pages
│   ├── index.js         # Home/dashboard page
│   ├── chat.js          # AI tutor workspace
│   ├── editor.js        # Code editor
│   ├── quiz.js          # Quiz interface
│   ├── progress.js      # Progress tracking
│   ├── teacher.js       # Teacher dashboard
│   ├── resources.js     # Resource library
│   └── api/             # API routes
│       └── tutor.js     # AI agent routing
├── styles/              # Styling files
│   ├── globals.css      # Global styles and design tokens
│   └── Home.module.css  # Legacy styles (if any)
└── public/              # Static assets
```

## 🚀 Getting Started

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

## 🤖 AI Agent Integration

The platform integrates with multiple backend services for AI functionality:

- **Triage Service**: Port 8000 - Query routing
- **Concepts Service**: Port 8001 - Concept explanations
- **Code Review Service**: Port 8002 - Code analysis
- **Debug Service**: Port 8003 - Error resolution
- **Exercise Service**: Port 8004 - Problem generation
- **Progress Service**: Port 8005 - Learning analytics

## 🎯 Learning Modules

The curriculum covers essential Python programming concepts:

1. **Basics**: Variables, data types, operators
2. **Control Flow**: Conditionals, loops, exceptions
3. **Data Structures**: Lists, tuples, dictionaries, sets
4. **Functions**: Definition, parameters, scope
5. **OOP**: Classes, objects, inheritance
6. **Files**: File handling, CSV, JSON
7. **Errors**: Exception handling, debugging
8. **Libraries**: Package management, APIs

## 📊 Mastery System

Progress is calculated using a weighted average:
- Exercises (40%)
- Quizzes (30%)
- Code Quality (20%)
- Consistency (10%)

Mastery levels:
- **Beginner** (0-40%): Red
- **Learning** (41-70%): Yellow
- **Proficient** (71-90%): Green
- **Mastered** (91-100%): Blue

## 🏆 Hackathon Features

This implementation was designed for hackathon competition with:
- AI-first interface design
- Modern, visually impressive UI
- Competitive against top LMS products
- Immediate judge appeal in under 60 seconds
- Cross-platform compatibility

## 🤝 Contributing

We welcome contributions to LearnFlow! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.