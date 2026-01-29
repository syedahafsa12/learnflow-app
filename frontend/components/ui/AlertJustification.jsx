import React from 'react';

const AlertJustification = ({ alert }) => {
  return (
    <div className="mt-6 p-8 bg-white border border-slate-200 rounded-[2.5rem] shadow-sm space-y-8 animate-in slide-in-from-top-4 duration-500">
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <p className="text-[10px] font-black text-indigo-500 uppercase tracking-widest">Reasoning Engine</p>
          <h4 className="text-2xl font-black text-slate-900 tracking-tight">Detection Justification</h4>
        </div>
        <span className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest ${
          alert.severity === 'high' ? 'bg-rose-100 text-rose-600' : 'bg-amber-100 text-amber-600'
        }`}>
          {alert.severity} Severity
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-6">
           <div className="space-y-2">
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Analysis Target</p>
              <div className="flex items-center space-x-3 p-4 bg-slate-50 rounded-2xl border border-slate-100">
                 <div className="w-10 h-10 rounded-xl bg-indigo-500 flex items-center justify-center text-white font-black text-xs">
                    {alert.student.charAt(0)}
                 </div>
                 <p className="text-sm font-bold text-slate-900">{alert.student}</p>
              </div>
           </div>

           <div className="space-y-2">
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Confidence Metrics</p>
              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100 flex items-end justify-between">
                 <div>
                    <p className="text-2xl font-black text-slate-900">92%</p>
                    <p className="text-[8px] font-black text-slate-400 uppercase tracking-widest mt-1 text-nowrap">Detection Certainty</p>
                 </div>
                 <div className="flex gap-1 h-8 items-end">
                    {[3, 5, 8, 4, 9, 7].map((h, i) => (
                      <div key={i} className="w-1 bg-indigo-500 rounded-full" style={{height: `${h*10}%`}}></div>
                    ))}
                 </div>
              </div>
           </div>
        </div>

        <div className="space-y-4">
           <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Primary Triggers</p>
           <div className="space-y-2">
              {alert.factors?.map((f, i) => (
                <div key={i} className="flex items-center space-x-3 p-4 bg-rose-50/50 border border-rose-100 rounded-2xl group transition-all hover:bg-rose-50">
                   <span className="text-rose-500 transition-transform group-hover:scale-125">⚡</span>
                   <span className="text-xs font-bold text-rose-900">{f}</span>
                </div>
              ))}
           </div>
        </div>
      </div>
      
      <div className="pt-8 border-t border-slate-100 flex flex-col md:flex-row gap-4">
         <button className="flex-1 btn-premium px-0">Direct Intervention ↗</button>
         <button className="flex-1 py-4 bg-white border border-slate-200 text-slate-500 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-50 hover:text-slate-900 transition-all">Dismiss Case</button>
      </div>
    </div>
  );
};

export default AlertJustification;