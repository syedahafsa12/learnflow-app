import React from 'react';

const Card = ({ children, className = '', title, subtitle, footer, noPadding = false, hover = true, glass = false }) => {
  return (
    <div className={`
      ${glass ? 'glass' : 'bg-white border border-slate-200/60'} 
      ${hover ? 'hover:shadow-xl hover:shadow-indigo-500/5 hover:-translate-y-1' : ''} 
      rounded-[2rem] overflow-hidden transition-all duration-500 flex flex-col h-full
      ${className}
    `}>
      {(title || subtitle) && (
        <div className="px-8 py-6 border-b border-slate-100/60 bg-white/50">
          {title && <h3 className="text-xl font-black tracking-tight text-slate-900">{title}</h3>}
          {subtitle && <p className="text-sm text-slate-500 mt-1 font-medium">{subtitle}</p>}
        </div>
      )}
      
      <div className={`flex-1 ${noPadding ? '' : 'p-8'}`}>
        {children}
      </div>

      {footer && (
        <div className="px-8 py-5 bg-slate-50/50 border-t border-slate-100/60 mt-auto">
          {footer}
        </div>
      )}
    </div>
  );
};

export default Card;