import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import AgentIndicator from '../components/ui/AgentIndicator';
import StruggleRadar from '../components/ui/StruggleRadar';
import ExplainMistakeButton from '../components/ui/ExplainMistakeButton';
import Button from '../components/ui/Button';
import { useUser } from '../context/UserContext';
import Card from '../components/ui/Card';

const ChatView = () => {
  const { user } = useUser();
  const [isHydrated, setIsHydrated] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'tutor',
      text: `Hello ${user?.name?.split(' ')[0] || 'Student'}! I'm your AI Python tutor. I can help explain concepts, debug code, provide exercises, and track your progress. How can I help you today?`,
      agent: 'triage',
      timestamp: new Date().toISOString(),
      agentIdentity: 'Triage Agent'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentAgent, setCurrentAgent] = useState('triage');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      const newMessage = {
        id: Date.now(),
        sender: 'student',
        text: input,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, newMessage]);
      const userInput = input;
      setInput('');
      setIsLoading(true);

      try {
        const response = await fetch('/api/tutor', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: userInput,
            userId: user.name,
            context: {
              history: messages.slice(-5).map(m => m.text),
              currentAgent: currentAgent
            }
          }),
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error || 'Failed to get response');

        const agentNames = {
          'triage': 'Triage Agent',
          'concepts': 'Concepts Agent',
          'code-review': 'Code Review Agent',
          'debug': 'Debug Agent',
          'exercise': 'Exercise Agent',
          'progress': 'Progress Agent'
        };

        let responseText = '';
        if (data.agent === 'concepts' && data.response.explanation) {
          responseText = `### ${data.response.concept}\n\n${data.response.explanation}\n\n#### Examples\n\`\`\`python\n${data.response.examples[0]}\n\`\`\`\n\n#### Common Pitfalls\n${data.response.common_mistakes.map(m => `* ${m}`).join('\n')}`;
        } else {
          responseText = data.response.message || data.response;
        }

        const aiResponse = {
          id: Date.now() + 1,
          sender: 'tutor',
          text: responseText,
          agent: data.agent,
          timestamp: new Date().toISOString(),
          agentIdentity: agentNames[data.agent] || 'AI Tutor',
          struggleDetection: data.struggleDetection
        };

        setMessages(prev => [...prev, aiResponse]);
        setCurrentAgent(data.agent);
      } catch (error) {
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          sender: 'tutor',
          text: '❌ **Connection Error**: I could not reach my specialized learning agents. Please ensure the backend is running.',
          agent: 'triage',
          agentIdentity: 'System'
        }]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const getAgentEmoji = (agent) => {
    return {
      triage: '🔄', concepts: '📚', 'code-review': '🔍',
      debug: '🐛', exercise: '✏️', progress: '📈'
    }[agent] || '🤖';
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] animate-in fade-in duration-700">
      {/* Agent Presence Header */}
      <div className="bg-white/80 backdrop-blur-md p-6 rounded-t-[2.5rem] border-x border-t border-slate-200/60 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-2xl bg-indigo-50 flex items-center justify-center text-2xl shadow-inner animate-float">
            {getAgentEmoji(currentAgent)}
          </div>
          <div>
            <h2 className="text-sm font-black text-slate-900 uppercase tracking-widest flex items-center space-x-2">
              <span>{currentAgent.replace('-', ' ')} Agent</span>
              <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse-soft"></span>
            </h2>
            <p className="text-xs text-slate-500 font-medium">Specifying educational context...</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-6">
          <div className="hidden sm:block">
            <StruggleRadar level={0} isActive={false} />
          </div>
          <div className="h-8 w-[1px] bg-slate-200"></div>
          <button className="text-xs font-black text-indigo-600 hover:text-indigo-800 transition-colors uppercase tracking-widest">
            Session History ↗
          </button>
        </div>
      </div>

      {/* Messages Window */}
      <div className="flex-1 bg-white border-x border-slate-200/60 overflow-y-auto px-8 py-10 space-y-8 custom-scrollbar">
        {messages.map((msg, i) => (
          <div key={msg.id} className={`flex ${msg.sender === 'student' ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2 duration-300`}>
            <div className={`max-w-[85%] sm:max-w-2xl group`}>
              <div className={`flex items-center space-x-2 mb-2 ${msg.sender === 'student' ? 'justify-end' : ''}`}>
                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                  {msg.sender === 'student' ? user.name : msg.agentIdentity}
                </span>
                {msg.sender !== 'student' && (
                  <span className="px-1.5 py-0.5 bg-slate-100 text-slate-500 rounded text-[8px] font-black uppercase">
                    v2.1
                  </span>
                )}
              </div>
              
              <div className={`
                relative p-5 rounded-3xl text-sm leading-relaxed shadow-sm
                ${msg.sender === 'student' 
                  ? 'bg-slate-900 text-white rounded-br-none font-medium' 
                  : 'bg-slate-50 text-slate-800 border border-slate-100 rounded-bl-none'}
              `}>
                <div className="prose prose-sm max-w-none prose-slate prose-headings:text-slate-900 prose-headings:font-black prose-a:text-indigo-600 prose-code:text-indigo-600 prose-code:bg-indigo-50 prose-code:px-1 prose-code:rounded prose-pre:bg-slate-900 prose-pre:rounded-2xl prose-pre:shadow-xl">
                  {msg.sender === 'student' ? (
                    <p>{msg.text}</p>
                  ) : (
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  )}
                </div>

                {msg.sender !== 'student' && msg.text.toLowerCase().includes('error') && (
                  <div className="mt-4 pt-4 border-t border-slate-200/60">
                    <ExplainMistakeButton error={msg.text} />
                  </div>
                )}
              </div>
              <p className={`mt-1.5 text-[8px] font-bold text-slate-400 uppercase tracking-widest ${msg.sender === 'student' ? 'text-right outline-none' : ''}`}>
                {isHydrated ? new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '...'}
              </p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start items-center space-x-4 animate-pulse">
            <div className="w-8 h-8 rounded-xl bg-slate-100 flex items-center justify-center grayscale">
              {getAgentEmoji(currentAgent)}
            </div>
            <div className="flex space-x-1.5">
              <div className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce"></div>
              <div className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce delay-75"></div>
              <div className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce delay-150"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Console */}
      <div className="bg-slate-50 p-6 rounded-b-[2.5rem] border border-slate-200/60 shadow-inner">
        <div className="max-w-4xl mx-auto space-y-4">
          <form onSubmit={handleSubmit} className="relative group">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about Python, or paste an error message..."
              className="w-full pl-6 pr-32 py-5 bg-white border border-slate-200 rounded-2xl shadow-sm focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 transition-all font-medium text-slate-900 placeholder-slate-400"
              disabled={isLoading}
            />
            <div className="absolute right-2 top-2 bottom-2">
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className={`h-full px-6 rounded-xl font-black text-xs uppercase tracking-widest transition-all shadow-md active:scale-95 ${
                  isLoading || !input.trim() 
                    ? 'bg-slate-100 text-slate-400 border border-slate-200' 
                    : 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-indigo-500/20'
                }`}
              >
                {isLoading ? 'Sending...' : 'Post Message →'}
              </button>
            </div>
          </form>
          
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest mr-1">Quick Prompts:</span>
            {['Explain Range', 'Review My Code', 'Practice Task', 'Next Module'].map((action) => (
              <button
                key={action}
                onClick={() => setInput(action)}
                className="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-[10px] font-bold text-slate-600 hover:border-indigo-400 hover:text-indigo-600 transition-all shadow-sm"
              >
                {action}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatView;