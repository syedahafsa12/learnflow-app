import React, { useState } from 'react';
import Card from './Card';
import Button from './Button';

const ExplainMistakeButton = ({ error }) => {
  const [showExplanation, setShowExplanation] = useState(false);

  return (
    <>
      <button
        onClick={() => setShowExplanation(true)}
        className="w-full flex items-center justify-center space-x-2 px-6 py-4 bg-rose-50 text-rose-700 rounded-2xl text-xs font-black uppercase tracking-widest border border-rose-100 hover:bg-rose-100 transition-all active:scale-95 shadow-sm"
      >
        <span>🔍</span>
        <span>Explain My Mistake</span>
      </button>

      {showExplanation && (
        <div className="fixed inset-0 bg-slate-900/80 backdrop-blur-md flex items-center justify-center z-[100] p-6 animate-in fade-in duration-300">
          <Card className="max-w-2xl w-full border-0 shadow-[0_0_100px_rgba(0,0,0,0.5)] !p-0 overflow-hidden rounded-[3rem] animate-in zoom-in-95 duration-300">
             <div className="bg-slate-950 px-8 py-6 flex items-center justify-between border-b border-slate-800">
                <div className="flex items-center space-x-3">
                   <div className="w-10 h-10 rounded-xl bg-rose-500 flex items-center justify-center text-xl shadow-lg shadow-rose-500/20">🔍</div>
                   <h3 className="text-xl font-black text-white tracking-tight">AI Error Analysis</h3>
                </div>
                <button
                  onClick={() => setShowExplanation(false)}
                  className="w-10 h-10 flex items-center justify-center bg-slate-800 text-slate-400 hover:text-white rounded-xl transition-all"
                >
                  <span className="text-2xl font-light">×</span>
                </button>
             </div>
             
             <div className="p-8 space-y-8 max-h-[70vh] overflow-y-auto custom-scrollbar">
                <div className="space-y-3">
                   <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Identified Exception</p>
                   <p className="text-sm font-mono text-rose-500 bg-rose-50 p-6 rounded-2xl border border-rose-100 leading-relaxed shadow-inner">
                     {error}
                   </p>
                </div>

                <div className="space-y-4">
                   <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Educational Breakdown</p>
                   <div className="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm">
                      <p className="text-slate-700 leading-relaxed font-medium">
                        "Your code attempted to perform an action that Python doesn't allow in this context. Specifically, you have a **SyntaxError** because of an unclosed parenthesis or missing colon."
                      </p>
                      <div className="mt-8 pt-8 border-t border-slate-100 grid grid-cols-2 gap-6">
                         <div>
                            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">The Cause</p>
                            <p className="text-xs text-slate-600 font-bold">Structural inconsistency in line 4.</p>
                         </div>
                         <div>
                            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Recommended Fix</p>
                            <p className="text-xs text-emerald-600 font-bold">Add a colon (:) after your 'if' statement.</p>
                         </div>
                      </div>
                   </div>
                </div>
                
                <div className="flex gap-4">
                   <Button variant="primary" className="flex-1" onClick={() => setShowExplanation(false)}>Got it, let me fix it!</Button>
                   <Button variant="outline" onClick={() => setShowExplanation(false)}>Add to Session Notes</Button>
                </div>
             </div>
          </Card>
        </div>
      )}
    </>
  );
};

export default ExplainMistakeButton;