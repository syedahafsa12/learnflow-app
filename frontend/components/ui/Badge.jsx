import React from 'react';

const Badge = ({ children, variant = 'default', size = 'md', className = '' }) => {
  const baseClasses = 'inline-flex items-center rounded-xl font-black uppercase tracking-widest transition-all duration-300';

  const variants = {
    default: 'bg-slate-100 text-slate-600 border border-slate-200',
    primary: 'bg-indigo-50 text-indigo-600 border border-indigo-100',
    success: 'bg-emerald-50 text-emerald-700 border border-emerald-100',
    warning: 'bg-amber-50 text-amber-700 border border-amber-100',
    danger: 'bg-rose-50 text-rose-700 border border-rose-100',
    info: 'bg-blue-50 text-blue-700 border border-blue-100',
    premium: 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white border-0 shadow-sm shadow-indigo-500/20'
  };

  const sizes = {
    sm: 'text-[8px] px-2 py-0.5',
    md: 'text-[10px] px-3 py-1',
    lg: 'text-xs px-4 py-1.5'
  };

  return (
    <span className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${className}`}>
      {children}
    </span>
  );
};

export default Badge;