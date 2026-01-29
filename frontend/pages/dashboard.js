import React from 'react';
import Card from '../components/ui/Card';
import ProgressBar from '../components/ui/ProgressBar';
import Badge from '../components/ui/Badge';
import Button from '../components/ui/Button';
import { useUser } from '../context/UserContext';

const DashboardView = () => {
  const { user } = useUser();
  const currentModule = { name: 'Control Flow', progress: 60, status: 'in-progress' };
  const streak = 5;
  const exercisesCompleted = 12;
  const masteryLevel = 'Learning';

  const modules = [
    { name: 'Basics', progress: 100, status: 'completed', icon: '🌱' },
    { name: 'Control Flow', progress: 60, status: 'in-progress', icon: '🔄' },
    { name: 'Data Structures', progress: 0, status: 'locked', icon: '📦' },
    { name: 'Functions', progress: 0, status: 'locked', icon: 'λ' },
    { name: 'OOP', progress: 0, status: 'locked', icon: '🏛️' },
  ];

  return (
    <div className="space-y-10 pb-12">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-[2.5rem] bg-slate-900 text-white p-10 shadow-2xl">
        <div className="absolute top-0 right-0 -mt-20 -mr-20 w-96 h-96 bg-indigo-500/20 rounded-full blur-[100px]"></div>
        <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-80 h-80 bg-purple-500/20 rounded-full blur-[80px]"></div>
        
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-8">
          <div className="space-y-4 max-w-xl">
            <div className="inline-flex items-center space-x-2 px-3 py-1 bg-white/10 backdrop-blur-md rounded-full border border-white/20">
              <span className="animate-pulse w-2 h-2 bg-indigo-400 rounded-full"></span>
              <span className="text-xs font-bold uppercase tracking-widest text-indigo-200">System Online</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-black tracking-tight leading-tight">
              Welcome back, <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 to-purple-300">{user?.name?.split(' ')[0] || 'Student'}</span>!
            </h1>
            <p className="text-slate-400 text-lg font-medium leading-relaxed">
              You're making incredible progress. Your AI tutor has prepared a new set of challenges based on your recent activity.
            </p>
            <div className="flex flex-wrap gap-4 pt-4">
              <button className="btn-premium">
                Continue Learning
              </button>
              <button className="px-6 py-3 rounded-2xl bg-white/5 hover:bg-white/10 border border-white/10 transition-colors font-bold text-sm backdrop-blur-sm">
                View Roadmap
              </button>
            </div>
          </div>

          <div className="flex-shrink-0">
            <div className="glass-dark p-8 rounded-[2rem] border border-white/5 shadow-inner">
              <div className="flex flex-col items-center">
                <div className="relative mb-6">
                  <svg className="w-32 h-32 transform -rotate-90">
                    <circle cx="64" cy="64" r="58" stroke="rgba(255,255,255,0.05)" strokeWidth="10" fill="none" />
                    <circle
                      cx="64" cy="64" r="58"
                      stroke="url(#hero-grad)"
                      strokeWidth="10"
                      fill="none"
                      strokeDasharray="364.4"
                      strokeDashoffset={364.4 * (1 - currentModule.progress / 100)}
                      strokeLinecap="round"
                    />
                    <defs>
                      <linearGradient id="hero-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#818cf8" />
                        <stop offset="100%" stopColor="#c084fc" />
                      </linearGradient>
                    </defs>
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-3xl font-black">{currentModule.progress}%</span>
                  </div>
                </div>
                <div className="text-center">
                  <p className="text-sm font-black text-indigo-300 uppercase tracking-widest mb-1">{currentModule.name}</p>
                  <p className="text-slate-400 text-xs font-medium">Topic Mastery: Developing</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Stats */}
        <div className="lg:col-span-2 space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="!p-6" hover={true}>
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 rounded-2xl bg-indigo-50 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">🔥</div>
                <Badge variant="success">Active</Badge>
              </div>
              <p className="text-3xl font-black text-slate-900">{streak}</p>
              <p className="text-sm font-medium text-slate-500">Day Streak</p>
            </Card>
            
            <Card className="!p-6" hover={true}>
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 rounded-2xl bg-purple-50 flex items-center justify-center text-2xl">✅</div>
                <Badge variant="info">Completed</Badge>
              </div>
              <p className="text-3xl font-black text-slate-900">{exercisesCompleted}</p>
              <p className="text-sm font-medium text-slate-500">Exercises Finished</p>
            </Card>

            <Card className="!p-6" hover={true}>
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 rounded-2xl bg-amber-50 flex items-center justify-center text-2xl">🧠</div>
                <Badge variant="warning">Learning</Badge>
              </div>
              <p className="text-3xl font-black text-slate-900">{masteryLevel}</p>
              <p className="text-sm font-medium text-slate-500">Global Proficiency</p>
            </Card>
          </div>

          <Card title="Python Learning Pathway" subtitle="Your personalized curriculum tracked by AI agents.">
            <div className="space-y-4">
              {modules.map((module, i) => (
                <div key={i} className={`group flex items-center p-5 rounded-2xl transition-all duration-300 border ${
                  module.status === 'completed' ? 'bg-indigo-50/30 border-indigo-100 hover:bg-indigo-50/50' : 
                  module.status === 'in-progress' ? 'bg-white border-slate-200 shadow-lg shadow-indigo-500/5 ring-1 ring-indigo-500/10' : 
                  'bg-slate-50 border-slate-100 opacity-60'
                }`}>
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-xl mr-5 shadow-sm ${
                    module.status === 'completed' ? 'bg-indigo-500 text-white' : 
                    module.status === 'in-progress' ? 'bg-white border border-indigo-200 text-indigo-500' : 
                    'bg-slate-200 text-slate-500'
                  }`}>
                    {module.status === 'completed' ? '✓' : module.icon}
                  </div>
                  <div className="flex-1">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className={`font-bold ${module.status === 'locked' ? 'text-slate-400' : 'text-slate-900'}`}>{module.name}</h4>
                      <span className="text-xs font-black text-slate-500 uppercase tracking-tighter">{module.progress}%</span>
                    </div>
                    <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div 
                        className={`h-full transition-all duration-1000 ${module.status === 'completed' ? 'bg-indigo-500' : 'bg-gradient-to-r from-indigo-500 to-purple-500'}`}
                        style={{ width: `${module.progress}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* AI Recommendations Side Panel */}
        <div className="space-y-8">
          <Card className="!bg-indigo-600 !text-white !p-0 overflow-hidden border-0" hover={true}>
            <div className="p-8 space-y-4 relative overflow-hidden">
               <div className="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-white/10 rounded-full blur-2xl"></div>
               <div className="inline-flex items-center space-x-2 px-3 py-1 bg-white/20 rounded-full text-[10px] font-black uppercase tracking-widest">
                AI Next Step
               </div>
               <h3 className="text-xl font-black">Control Flow Master</h3>
               <p className="text-indigo-100 text-sm leading-relaxed">
                 "You've crushed 60% of loops! Try the Quiz Master to unlock the next module."
               </p>
               <button className="w-full py-4 bg-white text-indigo-600 rounded-2xl font-black text-sm hover:bg-indigo-50 transition-colors shadow-xl">
                 Start Quiz Now
               </button>
            </div>
          </Card>

          <Card title="AI Specialist Activity" noPadding={true}>
             <div className="divide-y divide-slate-100">
               <div className="p-6 flex items-start space-x-4">
                 <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-lg shadow-sm">🤖</div>
                 <div>
                   <p className="text-sm font-bold text-slate-900">Triage Agent</p>
                   <p className="text-xs text-slate-500 mt-1">Analyzing your recent struggle with nested loops.</p>
                 </div>
               </div>
               <div className="p-6 flex items-start space-x-4">
                 <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center text-lg shadow-sm">🧠</div>
                 <div>
                   <p className="text-sm font-bold text-slate-900">Concepts Agent</p>
                   <p className="text-xs text-slate-500 mt-1">Found 3 new examples for "While Loops" you might like.</p>
                 </div>
               </div>
               <div className="p-6 flex items-start space-x-4">
                 <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-lg shadow-sm">💻</div>
                 <div>
                   <p className="text-sm font-bold text-slate-900">Code Review Agent</p>
                   <p className="text-xs text-slate-500 mt-1">Great job! Your solution for Exercise #12 was very efficient.</p>
                 </div>
               </div>
             </div>
          </Card>

          <Card title="Your Achievements" className="bg-slate-50/50">
            <div className="flex flex-wrap gap-3">
              <div className="w-12 h-12 rounded-full bg-white shadow-sm flex items-center justify-center text-xl grayscale hover:grayscale-0 transition-all cursor-help" title="Early Bird">🐣</div>
              <div className="w-12 h-12 rounded-full bg-white shadow-sm flex items-center justify-center text-xl cursor-help" title="Loop Legend">♾️</div>
              <div className="w-12 h-12 rounded-full bg-white shadow-sm flex items-center justify-center text-xl grayscale hover:grayscale-0 transition-all cursor-help" title="Clean Coder">✨</div>
              <div className="w-12 h-12 rounded-full bg-white shadow-sm flex items-center justify-center text-xl grayscale hover:grayscale-0 transition-all cursor-help" title="Fast Learner">⚡</div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default DashboardView;