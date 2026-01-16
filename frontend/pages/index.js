import Head from 'next/head';
import { useState } from 'react';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [user, setUser] = useState({ name: 'Student', role: 'student' });

  return (
    <div className={styles.container}>
      <Head>
        <title>LearnFlow - AI-Powered Python Learning</title>
        <meta name="description" content="AI-powered Python tutoring platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className={styles.header}>
        <div className={styles.logo}>LearnFlow</div>
        <nav className={styles.nav}>
          <button
            className={activeTab === 'dashboard' ? styles.active : ''}
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
          <button
            className={activeTab === 'chat' ? styles.active : ''}
            onClick={() => setActiveTab('chat')}
          >
            AI Tutor
          </button>
          <button
            className={activeTab === 'editor' ? styles.active : ''}
            onClick={() => setActiveTab('editor')}
          >
            Code Editor
          </button>
          <button
            className={activeTab === 'progress' ? styles.active : ''}
            onClick={() => setActiveTab('progress')}
          >
            Progress
          </button>
        </nav>
        <div className={styles.user}>
          Welcome, {user.name} ({user.role})
        </div>
      </header>

      <main className={styles.main}>
        {activeTab === 'dashboard' && (
          <DashboardView />
        )}
        {activeTab === 'chat' && (
          <ChatView />
        )}
        {activeTab === 'editor' && (
          <EditorView />
        )}
        {activeTab === 'progress' && (
          <ProgressView />
        )}
      </main>

      <footer className={styles.footer}>
        LearnFlow AI-Powered Python Learning Platform
      </footer>
    </div>
  );
}

function DashboardView() {
  return (
    <div className={styles.view}>
      <h1>Learning Dashboard</h1>
      <div className={styles.statsGrid}>
        <div className={styles.statCard}>
          <h3>Current Module</h3>
          <p>Control Flow - 60% Complete</p>
        </div>
        <div className={styles.statCard}>
          <h3>Streak</h3>
          <p>5 days</p>
        </div>
        <div className={styles.statCard}>
          <h3>Exercises Completed</h3>
          <p>12/15</p>
        </div>
        <div className={styles.statCard}>
          <h3>Mastery Level</h3>
          <p>Learning</p>
        </div>
      </div>

      <div className={styles.modulesSection}>
        <h2>Python Curriculum</h2>
        <div className={styles.modulesList}>
          {[
            { name: 'Basics', progress: 100, status: 'completed' },
            { name: 'Control Flow', progress: 60, status: 'in-progress' },
            { name: 'Data Structures', progress: 0, status: 'locked' },
            { name: 'Functions', progress: 0, status: 'locked' },
            { name: 'OOP', progress: 0, status: 'locked' },
            { name: 'Files', progress: 0, status: 'locked' },
            { name: 'Errors', progress: 0, status: 'locked' },
            { name: 'Libraries', progress: 0, status: 'locked' },
          ].map((module, index) => (
            <div key={index} className={`${styles.moduleItem} ${styles[module.status]}`}>
              <span className={styles.moduleName}>{module.name}</span>
              <div className={styles.progressBar}>
                <div
                  className={styles.progressFill}
                  style={{ width: `${module.progress}%` }}
                ></div>
              </div>
              <span className={styles.progressText}>{module.progress}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function ChatView() {
  const [messages, setMessages] = useState([
    { id: 1, sender: 'tutor', text: 'Hello! I\'m your Python tutor. What would you like to learn today?' }
  ]);
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      const newMessage = {
        id: messages.length + 1,
        sender: 'student',
        text: input
      };
      setMessages([...messages, newMessage]);
      setInput('');

      // Simulate AI response
      setTimeout(() => {
        const aiResponse = {
          id: messages.length + 2,
          sender: 'tutor',
          text: 'I understand you\'re asking about "' + input + '". Let me explain this Python concept...'
        };
        setMessages(prev => [...prev, aiResponse]);
      }, 1000);
    }
  };

  return (
    <div className={styles.view}>
      <h1>AI Python Tutor</h1>
      <div className={styles.chatContainer}>
        <div className={styles.messages}>
          {messages.map(msg => (
            <div key={msg.id} className={`${styles.message} ${styles[msg.sender]}`}>
              <div className={styles.messageText}>{msg.text}</div>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className={styles.chatInputForm}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about Python concepts, errors, or anything else..."
            className={styles.chatInput}
          />
          <button type="submit" className={styles.sendButton}>Send</button>
        </form>
      </div>
    </div>
  );
}

function EditorView() {
  const [code, setCode] = useState(`# Write your Python code here
def hello_world():
    return "Hello, World!"

print(hello_world())`);

  const [output, setOutput] = useState('');

  const runCode = () => {
    // In a real app, this would send code to a backend execution service
    setOutput('Code executed successfully! Output would appear here.');
  };

  return (
    <div className={styles.view}>
      <h1>Python Code Editor</h1>
      <div className={styles.editorContainer}>
        <div className={styles.editorHeader}>
          <button onClick={runCode} className={styles.runButton}>▶ Run Code</button>
          <button className={styles.saveButton}>Save</button>
        </div>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className={styles.codeEditor}
          spellCheck="false"
        />
        <div className={styles.outputPanel}>
          <h3>Output:</h3>
          <pre className={styles.outputContent}>{output}</pre>
        </div>
      </div>
    </div>
  );
}

function ProgressView() {
  return (
    <div className={styles.view}>
      <h1>Your Learning Progress</h1>
      <div className={styles.progressOverview}>
        <div className={styles.overviewCard}>
          <h3>Overall Mastery</h3>
          <div className={styles.masteryCircle}>
            <div className={styles.masteryPercentage}>60%</div>
          </div>
          <p>Learning Level</p>
        </div>

        <div className={styles.topicMastery}>
          <h3>Topic Mastery</h3>
          <div className={styles.masteryList}>
            {[
              { topic: 'Variables', mastery: 85, level: 'Proficient' },
              { topic: 'Control Flow', mastery: 60, level: 'Learning' },
              { topic: 'Functions', mastery: 45, level: 'Beginner' },
              { topic: 'Data Structures', mastery: 20, level: 'Beginner' },
            ].map((item, index) => (
              <div key={index} className={styles.masteryItem}>
                <span className={styles.topicName}>{item.topic}</span>
                <div className={styles.masteryBar}>
                  <div
                    className={styles.masteryFill}
                    style={{ width: `${item.mastery}%` }}
                  ></div>
                </div>
                <span className={styles.masteryPercent}>{item.mastery}%</span>
                <span className={styles.masteryLevel}>{item.level}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}