import React, { useState } from 'react';
import Card from '../components/ui/Card';
import ProgressBar from '../components/ui/ProgressBar';
import Badge from '../components/ui/Badge';
import { useUser } from '../context/UserContext';

const ProgressView = () => {
  const { user } = useUser();
  const [selectedTopic, setSelectedTopic] = useState(null);

  const progressData = {
    overallMastery: 68,
    masteryLevel: 'Learning',
    topics: [
      { topic: 'Variables', mastery: 85, level: 'Proficient', icon: '🌱' },
      { topic: 'Control Flow', mastery: 60, level: 'Learning', icon: '🔄' },
      { topic: 'Functions', mastery: 45, level: 'Beginner', icon: 'λ' },
      { topic: 'Data Structures', mastery: 20, level: 'Beginner', icon: '📦' },
      { topic: 'OOP', mastery: 10, level: 'Beginner', icon: '🏛️' }
    ]
  };

  return (
    <div className="space-y-10 pb-12 animate-in fade-in duration-700">
      <div className="space-y-2">
        <div className="inline-flex items-center space-x-2 px-3 py-1 bg-emerald-50 text-emerald-700 rounded-full text-[10px] font-black uppercase tracking-widest ring-1 ring-emerald-200">
          Learning Analytics
        </div>
        <h1 className="text-4xl font-black tracking-tight text-slate-900">Your Learning Journey</h1>
        <p className="text-slate-500 font-medium">Visualizing your growth as a Python developer.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <Card className="lg:col-span-1 !bg-slate-900 !text-white !p-10 border-0 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-indigo-500/20 rounded-full blur-3xl"></div>
          <div className="relative z-10 text-center space-y-8">
            <h3 className="text-sm font-black text-indigo-300 uppercase tracking-[0.2em]">Overall Mastery</h3>
            <div className="relative w-48 h-48 mx-auto">
              <svg className="w-48 h-48 transform -rotate-90">
                <circle cx="96" cy="96" r="88" stroke="rgba(255,255,255,0.05)" strokeWidth="12" fill="none" />
                <circle
                  cx="96" cy="96" r="88"
                  stroke="url(#prog-grad)"
                  strokeWidth="12"
                  fill="none"
                  strokeDasharray="552.9"
                  strokeDashoffset={552.9 * (1 - progressData.overallMastery / 100)}
                  strokeLinecap="round"
                />
                <defs>
                   <linearGradient id="prog-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#818cf8" />
                      <stop offset="100%" stopColor="#c084fc" />
                   </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-5xl font-black">{progressData.overallMastery}%</span>
                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest mt-1">{progressData.masteryLevel}</span>
              </div>
            </div>
            <div className="pt-4 space-y-2 underline-none">
              <Badge variant="premium" size="lg">Level 4: Python Pioneer</Badge>
              <p className="text-xs text-slate-500 font-medium leading-relaxed">
                You're in the top 15% of students in the {progressData.masteryLevel} bracket.
              </p>
            </div>
          </div>
        </Card>

        <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
           <Card title="Engagement Stats" className="h-fit">
              <div className="space-y-6">
                 <div className="flex justify-between items-end">
                    <div>
                       <p className="text-2xl font-black text-slate-900">12.5h</p>
                       <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Time Focused</p>
                    </div>
                    <div className="text-emerald-500 text-xs font-black">↑ 12% wk</div>
                 </div>
                 <ProgressBar value={75} max={100} showLabel={false} variant="success" />
                 
                 <div className="flex justify-between items-end pt-4">
                    <div>
                       <p className="text-2xl font-black text-slate-900">42</p>
                       <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Tasks Solved</p>
                    </div>
                    <div className="text-indigo-500 text-xs font-black">↑ 8 new</div>
                 </div>
                 <ProgressBar value={60} max={100} showLabel={false} />
              </div>
           </Card>

           <Card title="Skill Breakdown" className="h-fit">
              <div className="space-y-4">
                 {[
                   { label: 'Logic', val: 82, color: 'bg-emerald-500' },
                   { label: 'Syntax', val: 65, color: 'bg-indigo-500' },
                   { label: 'Debugging', val: 40, color: 'bg-amber-500' },
                   { label: 'Optimization', val: 25, color: 'bg-rose-500' }
                 ].map((s, i) => (
                   <div key={i} className="space-y-1.5">
                      <div className="flex justify-between text-[10px] font-black uppercase tracking-widest">
                         <span className="text-slate-500">{s.label}</span>
                         <span className="text-slate-900">{s.val}%</span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                         <div className={`h-full ${s.color}`} style={{width: `${s.val}%`}}></div>
                      </div>
                   </div>
                 ))}
              </div>
           </Card>
        </div>
      </div>

      <Card title="Module Proficiency Heatmap">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
            {progressData.topics.map((topic, i) => (
              <div key={i} className="p-6 rounded-[2rem] bg-slate-50 border border-slate-100 hover:bg-white hover:border-indigo-200 hover:shadow-xl hover:shadow-indigo-500/5 transition-all duration-300 group cursor-default">
                 <div className="text-3xl mb-4 group-hover:scale-110 transition-transform">
                   {topic.icon}
                 </div>
                 <h4 className="text-sm font-black text-slate-900 mb-2 truncate">{topic.topic}</h4>
                 <div className="flex items-center space-x-2">
                    <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{topic.mastery}%</span>
                    <div className="flex-1 h-1 bg-slate-200 rounded-full overflow-hidden">
                       <div className="h-full bg-indigo-500" style={{width: `${topic.mastery}%`}}></div>
                    </div>
                 </div>
                 <div className="mt-4">
                    <Badge variant={topic.level === 'Proficient' ? 'success' : topic.level === 'Learning' ? 'warning' : 'default'} size="sm">
                       {topic.level}
                    </Badge>
                 </div>
              </div>
            ))}
          </div>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
         <Card title="Recent Achievements" className="md:col-span-2">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-6">
               {[
                 { icon: '🏆', name: 'Variable Virtuoso' },
                 { icon: '⚡', name: 'Quick Fixer' },
                 { icon: '🔥', name: '7-Day Streak' },
                 { icon: '🧠', name: 'Logic Master' }
               ].map((a, i) => (
                 <div key={i} className="flex flex-col items-center space-y-3 p-4 rounded-3xl hover:bg-slate-50 transition-colors">
                    <div className="w-16 h-16 rounded-2xl bg-white shadow-sm border border-slate-100 flex items-center justify-center text-3xl">{a.icon}</div>
                    <span className="text-[10px] font-black text-center text-slate-600 uppercase tracking-widest leading-tight">{a.name}</span>
                 </div>
               ))}
            </div>
         </Card>
         
         <Card className="!bg-indigo-600 !text-white overflow-hidden border-0">
            <div className="space-y-4">
               <h3 className="text-xl font-black tracking-tight leading-tight">AI Prediction</h3>
               <p className="text-indigo-100 text-sm font-medium leading-relaxed opacity-80">
                 "Based on your 85% mastery in Variables, we predict you'll reach Functions mastery in 4.2 days if you maintain your current streak."
               </p>
               <button className="w-full py-4 bg-white/10 hover:bg-white/20 transition-all rounded-2xl text-[10px] font-black uppercase tracking-widest border border-white/20">
                 View Predicted Roadmap ↗
               </button>
            </div>
         </Card>
      </div>
    </div>
  );
};

export default ProgressView;