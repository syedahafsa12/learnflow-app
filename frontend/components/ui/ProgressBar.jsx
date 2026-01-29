import React from 'react';

const ProgressBar = ({ value = 0, max = 100, variant = 'default', showLabel = false, className = '' }) => {
  const percentage = Math.min(Math.max(0, value / max * 100), 100);

  const variants = {
    default: 'bg-indigo-600',
    success: 'bg-emerald-500',
    warning: 'bg-amber-500',
    danger: 'bg-rose-500',
    premium: 'bg-gradient-to-r from-indigo-500 to-purple-600'
  };

  return (
    <div className={`w-full space-y-2 ${className}`}>
      <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden border border-slate-200/50 shadow-inner">
        <div
          className={`h-full rounded-full transition-all duration-1000 ease-out ${variants[variant] || variants.default}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
      {showLabel && (
        <div className="flex justify-between items-center text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">
          <span>Progress</span>
          <span className="text-slate-900">{Math.round(percentage)}%</span>
        </div>
      )}
    </div>
  );
};

export default ProgressBar;