import React, { useState } from 'react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Alert from '../components/ui/Alert';
import { useUser } from '../context/UserContext';

const EditorView = () => {
  const { user } = useUser();
  const [code, setCode] = useState(`# Write your Python code here
def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"Fibonacci of 10 is: {fibonacci(10)}")`);

  const [output, setOutput] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionStatus, setExecutionStatus] = useState('ready');

  const runCode = async () => {
    setIsExecuting(true);
    setExecutionStatus('executing');
    setOutput('🚀 Launching sandboxed environment...\n');

    try {
      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: code,
          user_id: user?.name || 'anonymous',
          timeout: 5,
          memoryLimit: 50
        }),
      });

      const result = await response.json();

      if (response.ok) {
        let outputText = '';
        if (result.output) outputText += result.output;
        if (result.error) outputText += `\n\n❌ RUNTIME ERROR:\n${result.error}`;

        if (result.execution_time !== undefined) {
          outputText += `\n\n------------------------------`;
          outputText += `\n⚡ Execution time: ${result.execution_time.toFixed(3)}s`;
          outputText += `\n✅ Success: ${result.success ? 'True' : 'False'}`;
        }

        setOutput(outputText);
        setExecutionStatus(result.success ? 'success' : 'error');
      } else {
        setOutput(`🚨 System Error: ${result.error || 'Failed to communicate with backend'}`);
        setExecutionStatus('error');
      }
    } catch (error) {
      setOutput(`🌐 Network Error: ${error.message}\nEnsure backend agents are running.`);
      setExecutionStatus('error');
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="px-1 py-1 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-indigo-50 text-indigo-700 rounded-full text-[10px] font-black uppercase tracking-widest ring-1 ring-indigo-200">
            Interactive Environment
          </div>
          <h1 className="text-4xl font-black tracking-tight text-slate-900">Python Code Lab</h1>
          <p className="text-slate-500 font-medium">Experiment, build, and learn with real-time AI feedback.</p>
        </div>
        
        <div className="flex items-center gap-3">
          <div className={`flex items-center space-x-2 px-4 py-2 rounded-2xl text-sm font-bold shadow-sm border transition-all duration-300 ${
            executionStatus === 'ready' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' :
            executionStatus === 'executing' ? 'bg-amber-50 text-amber-700 border-amber-100 animate-pulse' :
            'bg-rose-50 text-rose-700 border-rose-100'
          }`}>
            <span className="text-base">
              {executionStatus === 'ready' && '🟢'}
              {executionStatus === 'executing' && '⏳'}
              {executionStatus === 'error' && '🔴'}
              {executionStatus === 'success' && '✨'}
            </span>
            <span>{executionStatus.toUpperCase()}</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <div className="lg:col-span-8 space-y-6">
          <Card className="!p-0 border-0 shadow-2xl overflow-hidden ring-1 ring-slate-200" noPadding={true}>
            {/* Editor Toolbar */}
            <div className="bg-slate-900 px-6 py-4 flex items-center justify-between border-b border-slate-700">
              <div className="flex items-center space-x-4">
                <button
                  onClick={runCode}
                  disabled={isExecuting}
                  className={`
                    flex items-center space-x-2 px-6 py-2.5 rounded-xl font-black text-sm transition-all shadow-lg
                    ${isExecuting 
                      ? 'bg-slate-800 text-slate-500 cursor-not-allowed' 
                      : 'bg-indigo-500 text-white hover:bg-indigo-400 active:scale-95 shadow-indigo-500/20'}
                  `}
                >
                  <span className="text-lg">{isExecuting ? '⌛' : '▶'}</span>
                  <span>{isExecuting ? 'Running...' : 'Run Code'}</span>
                </button>

                <button className="p-2.5 bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white rounded-xl transition-all shadow-sm">
                  💾
                </button>
                
                <div className="h-6 w-[1px] bg-slate-700 mx-1"></div>
                
                <select className="bg-slate-800 text-slate-300 border-0 rounded-xl px-4 py-2.5 text-xs font-bold hover:bg-slate-700 outline-none cursor-pointer tracking-wide">
                  <option>main.py</option>
                  <option>utils.py</option>
                  <option>data.csv</option>
                </select>
              </div>

              <div className="flex items-center space-x-4">
                <div className="hidden sm:flex items-center space-x-2 text-[10px] font-black text-slate-500 uppercase tracking-widest bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
                  <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></span>
                  <span>Python 3.10</span>
                </div>
              </div>
            </div>

            {/* Code Field */}
            <div className="relative group">
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="w-full h-[500px] font-mono text-sm bg-slate-900 text-indigo-100 p-8 focus:outline-none resize-none leading-relaxed custom-scrollbar selection:bg-indigo-500/30"
                spellCheck="false"
                placeholder="Write your Python code here..."
              />
              <div className="absolute inset-y-0 left-0 w-12 bg-slate-950/50 border-r border-slate-800 flex flex-col items-center py-8 text-[10px] font-mono text-slate-600 select-none">
                {Array.from({length: 20}).map((_, i) => <div key={i} className="h-5 flex items-center">{i+1}</div>)}
              </div>
            </div>

            {/* Terminal Output */}
            <div className="bg-slate-950 border-t border-slate-800">
              <div className="flex items-center justify-between px-6 py-3 border-b border-slate-900 bg-slate-900/50">
                <div className="flex items-center space-x-2">
                  <span className="text-slate-500">❯</span>
                  <h3 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Console Output</h3>
                </div>
                <button
                  onClick={() => setOutput('')}
                  className="text-[10px] font-black text-slate-500 hover:text-rose-400 uppercase tracking-widest transition-colors flex items-center space-x-1"
                >
                  <span>🗑️</span>
                  <span>Clear</span>
                </button>
              </div>
              <pre className="p-8 text-sm font-mono text-indigo-300 whitespace-pre-wrap h-48 overflow-y-auto custom-scrollbar selection:bg-indigo-500/30">
                {output || <span className="text-slate-700 italic opacity-50">Program output will appear here after execution...</span>}
              </pre>
            </div>
          </Card>
        </div>

        <div className="lg:col-span-4 space-y-6">
          <Card title="Environment Specs" className="bg-slate-50/50 border-slate-200">
            <div className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">🔒 Sandbox</span>
                  <span className="text-xs font-black text-indigo-600">Strict Isolation</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">⏱️ Timeout</span>
                  <span className="text-xs font-black text-slate-900">5 Seconds</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">💾 Memory</span>
                  <span className="text-xs font-black text-slate-900">50 MB</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">🌐 Network</span>
                  <span className="text-xs font-black text-rose-500">Disabled</span>
                </div>
              </div>
            </div>
          </Card>

          <Card className="bg-gradient-to-br from-indigo-500 to-purple-600 !text-white border-0 shadow-lg shadow-indigo-500/20">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-xl bg-white/20 backdrop-blur-md flex items-center justify-center text-xl">💡</div>
                <h3 className="text-lg font-black">AI Tip</h3>
              </div>
              <p className="text-indigo-100 text-sm font-medium leading-relaxed">
                "Not sure what to write? Click the 'Load Sample' button above to see examples of loops, functions, and more!"
              </p>
              <button className="w-full py-3 bg-white/10 hover:bg-white/20 transition-all rounded-xl text-xs font-black uppercase tracking-widest border border-white/20">
                Learn syntax ↗
              </button>
            </div>
          </Card>

          <div className="p-6 bg-amber-50 rounded-[2rem] border border-amber-200 shadow-sm">
             <div className="flex items-center space-x-3 mb-4">
               <span className="text-xl">🛡️</span>
               <h4 className="text-sm font-black text-amber-900 uppercase tracking-wider">Privacy Note</h4>
             </div>
             <p className="text-xs text-amber-800 font-medium leading-relaxed opacity-80">
               Your code is executed in a temporary, stateless container. Files created during execution are automatically deleted.
             </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EditorView;