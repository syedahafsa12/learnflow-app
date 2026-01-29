import React from 'react';

const StruggleRadar = ({ level, isActive }) => {
  return (
    <div className={`
      flex items-center space-x-4 px-6 py-3 rounded-2xl border transition-all duration-500
      ${isActive 
        ? 'bg-rose-50 border-rose-200 shadow-lg shadow-rose-500/10' 
        : 'bg-indigo-50 border-indigo-100 shadow-sm'}
    `}>
      <div className={`relative flex items-center justify-center ${isActive ? 'animate-pulse' : ''}`}>
        <span className="text-xl">{isActive ? '⚠️' : '🛡️'}</span>
      </div>
      
      <div className="flex flex-col">
        <span className={`text-[10px] font-black uppercase tracking-widest ${isActive ? 'text-rose-600' : 'text-indigo-600'}`}>
          {isActive ? 'Struggle Alert' : 'Safety Net'}
        </span>
        <span className={`text-[8px] font-bold text-slate-400 uppercase tracking-widest mt-0.5`}>
          {isActive ? 'Immediate Intervention' : 'Monitoring Active'}
        </span>
      </div>

      {isActive && (
        <div className="w-20 bg-rose-100 rounded-full h-1.5 overflow-hidden">
          <div
            className="h-full bg-rose-500 rounded-full transition-all duration-1000"
            style={{ width: `${level}%` }}
          ></div>
        </div>
      )}
    </div>
  );
};

export default StruggleRadar;