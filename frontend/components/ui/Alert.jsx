import React from 'react';

const Alert = ({ children, variant = 'info', title, icon = null, className = '' }) => {
  const variants = {
    info: 'bg-blue-50/50 border-blue-100 text-blue-900',
    success: 'bg-emerald-50/50 border-emerald-100 text-emerald-900',
    warning: 'bg-amber-50/50 border-amber-100 text-amber-900',
    danger: 'bg-rose-50/50 border-rose-100 text-rose-900'
  };

  const icons = { info: 'ℹ️', success: '✅', warning: '⚠️', danger: '🚨' };

  return (
    <div className={`
      relative overflow-hidden p-6 rounded-[2rem] border transition-all duration-300
      ${variants[variant] || variants.info} ${className}
    `}>
      <div className="flex gap-4">
        <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-white/50 backdrop-blur-md flex items-center justify-center text-xl shadow-sm">
           {icon || icons[variant]}
        </div>
        <div className="space-y-1">
          {title && <h3 className="text-sm font-black uppercase tracking-widest">{title}</h3>}
          <div className="text-sm font-medium opacity-80 leading-relaxed">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Alert;