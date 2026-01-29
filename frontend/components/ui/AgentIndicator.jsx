import React from 'react';

const AgentIndicator = ({ agent, status, reason }) => {
  const agentGradients = {
    'triage': 'linear-gradient(135deg, #a855f7, #ec4899)',
    'concepts': 'linear-gradient(135deg, #3b82f6, #06b6d4)',
    'code-review': 'linear-gradient(135deg, #22c55e, #10b981)',
    'debug': 'linear-gradient(135deg, #ef4444, #f43f5e)',
    'exercise': 'linear-gradient(135deg, #eab308, #f59e0b)',
    'progress': 'linear-gradient(135deg, #6b7280, #64748b)'
  };

  return (
    <div className="flex items-center space-x-4 p-4 bg-white/50 backdrop-blur-md rounded-2xl border border-slate-200/60 shadow-sm transition-all hover:shadow-md">
      <div className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-black text-xs shadow-lg animate-float" style={{background: agentGradients[agent] || agentGradients.progress}}>
        {agent.charAt(0).toUpperCase()}
      </div>
      <div>
        <div className="flex items-center space-x-2">
           <p className="text-[10px] font-black text-slate-900 uppercase tracking-widest leading-none capitalize">{agent} Agent</p>
           <span className={`w-2 h-2 rounded-full ${status === 'active' ? 'bg-emerald-500 animate-pulse' : 'bg-slate-300'}`}></span>
        </div>
        <p className="text-[10px] text-slate-500 font-bold mt-1 max-w-[150px] truncate">{reason}</p>
      </div>
    </div>
  );
};

export default AgentIndicator;