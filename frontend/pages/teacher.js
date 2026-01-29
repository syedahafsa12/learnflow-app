import React, { useState } from 'react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import ProgressBar from '../components/ui/ProgressBar';
import Badge from '../components/ui/Badge';
import Alert from '../components/ui/Alert';
import AlertJustification from '../components/ui/AlertJustification';
import { useUser } from '../context/UserContext';
import Link from 'next/link';

const TeacherDashboardView = () => {
  const { user } = useUser();
  const [activeTab, setActiveTab] = useState('overview');

  if (!user) return <div className="p-10 text-center">Loading context...</div>;

  // Restricted Access UI for Students
  if (user.role !== 'teacher') {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-8 text-center animate-in fade-in zoom-in duration-500">
        <div className="w-32 h-32 bg-rose-50 rounded-[2.5rem] flex items-center justify-center text-5xl shadow-inner animate-float">🔒</div>
        <div className="space-y-3 max-w-md">
          <h1 className="text-4xl font-black tracking-tight text-slate-900">Restricted Access</h1>
          <p className="text-slate-500 font-medium leading-relaxed">
            The Teacher Hub is exclusively for educators. You can switch to the Teacher role from the dashboard to explore this area.
          </p>
        </div>
        <Link href="/">
           <button className="btn-premium px-10">Back to Dashboard</button>
        </Link>
      </div>
    );
  }

  // Teacher Data
  const classList = [
    { id: 1, name: 'Maya Johnson', progress: 68, module: 'Control Flow', status: 'active', mastery: 'learning', engagement: 85 },
    { id: 2, name: 'James Wilson', progress: 45, module: 'List Comprehensions', status: 'struggling', mastery: 'beginner', engagement: 45 },
    { id: 3, name: 'Alex Rivera', progress: 85, module: 'Functions', status: 'proficient', mastery: 'proficient', engagement: 92 },
    { id: 4, name: 'Sam Taylor', progress: 25, module: 'Basics', status: 'beginner', mastery: 'beginner', engagement: 35 },
  ];

  const struggleAlerts = [
    { id: 1, student: 'James Wilson', issue: 'Struggling with list comprehensions', timestamp: '2 mins ago', severity: 'high', agentTriggered: 'concepts', factors: ['Same error 3+ times', 'Quiz score < 50%'] },
    { id: 2, student: 'Sam Taylor', issue: 'Stuck on basics quiz', timestamp: '1 hour ago', severity: 'medium', agentTriggered: 'exercise', factors: ['Quiz score < 40%'] },
  ];

  return (
    <div className="space-y-10 pb-12 animate-in fade-in duration-700">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-[10px] font-black uppercase tracking-widest ring-1 ring-purple-200">
            Education Intelligence
          </div>
          <h1 className="text-4xl font-black tracking-tight text-slate-900">Teacher Command Center</h1>
          <p className="text-slate-500 font-medium">Monitoring {classList.length} students across 8 learning modules.</p>
        </div>
        
        <div className="flex items-center bg-white p-1.5 rounded-2xl shadow-sm border border-slate-200/60">
           {['overview', 'alerts', 'roster'].map(t => (
             <button
               key={t}
               onClick={() => setActiveTab(t)}
               className={`px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${
                 activeTab === t ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'text-slate-500 hover:text-slate-900'
               }`}
             >
               {t}
             </button>
           ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <Card className="!p-6 !bg-rose-50 border-rose-100">
           <p className="text-xs font-black text-rose-500 uppercase tracking-widest mb-1">Active Alerts</p>
           <h4 className="text-3xl font-black text-rose-900">{struggleAlerts.length}</h4>
           <div className="mt-4 p-2 bg-white/50 rounded-lg text-[10px] font-bold text-rose-700 border border-rose-200/50">
             Immediate action recommended
           </div>
        </Card>
        <Card className="!p-6 !bg-indigo-50 border-indigo-100">
           <p className="text-xs font-black text-indigo-500 uppercase tracking-widest mb-1">Class Avg</p>
           <h4 className="text-3xl font-black text-indigo-900">72%</h4>
           <div className="mt-4 p-2 bg-white/50 rounded-lg text-[10px] font-bold text-indigo-700 border border-indigo-200/50">
             +4% increase this week
           </div>
        </Card>
        <Card className="!p-6 !bg-emerald-50 border-emerald-100">
           <p className="text-xs font-black text-emerald-500 uppercase tracking-widest mb-1">Proficiency</p>
           <h4 className="text-3xl font-black text-emerald-900">2/4</h4>
           <div className="mt-4 p-2 bg-white/50 rounded-lg text-[10px] font-bold text-emerald-700 border border-emerald-200/50">
             Students above threshold
           </div>
        </Card>
        <Card className="!p-6 !bg-purple-50 border-purple-100">
           <p className="text-xs font-black text-purple-500 uppercase tracking-widest mb-1">Engage Rate</p>
           <h4 className="text-3xl font-black text-purple-900">88%</h4>
           <div className="mt-4 p-2 bg-white/50 rounded-lg text-[10px] font-bold text-purple-700 border border-purple-200/50">
             High participation detected
           </div>
        </Card>
      </div>

      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card title="Struggle Detection Alerts">
            <div className="space-y-4">
              {struggleAlerts.map(alert => (
                <div key={alert.id} className="p-6 rounded-3xl bg-white border border-slate-200 hover:border-indigo-300 transition-colors shadow-sm">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center font-bold text-slate-600 border-2 border-white shadow-sm ring-1 ring-slate-200">
                        {alert.student.charAt(0)}
                      </div>
                      <div>
                        <h5 className="text-sm font-black text-slate-900">{alert.student}</h5>
                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{alert.timestamp}</p>
                      </div>
                    </div>
                    <Badge variant={alert.severity === 'high' ? 'danger' : 'warning'}>{alert.severity} Priority</Badge>
                  </div>
                  <div className="mb-4 bg-slate-50 p-4 rounded-2xl border border-slate-100">
                    <p className="text-sm font-bold text-slate-800 flex items-center">
                      <span className="mr-2">⚠️</span> {alert.issue}
                    </p>
                    <div className="mt-2 flex flex-wrap gap-2">
                      {alert.factors.map((f, i) => (
                        <span key={i} className="text-[10px] font-bold text-slate-500 bg-white px-2 py-0.5 rounded-full border border-slate-200">{f}</span>
                      ))}
                    </div>
                  </div>
                  <div className="flex gap-3">
                     <button className="flex-1 py-3 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-indigo-700 shadow-lg shadow-indigo-500/20 active:scale-95 transition-all">
                       Analyze Code ↗
                     </button>
                     <button className="px-6 py-3 bg-white border border-slate-200 text-slate-600 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-50 transition-all">
                       Hint
                     </button>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card title="Student Roster Quick-View">
            <div className="divide-y divide-slate-100/60">
              {classList.map(student => (
                <div key={student.id} className="py-5 flex items-center justify-between group cursor-default first:pt-0 last:pb-0">
                  <div className="flex items-center space-x-4">
                     <div className="relative">
                        <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center font-bold text-slate-600 border border-slate-200">
                          {student.name.charAt(0)}
                        </div>
                        <span className={`absolute -bottom-1 -right-1 w-3.5 h-3.5 border-2 border-white rounded-full ${
                          student.status === 'active' ? 'bg-emerald-500' : 
                          student.status === 'struggling' ? 'bg-rose-500' : 'bg-indigo-500'
                        }`}></span>
                     </div>
                     <div>
                       <h5 className="text-sm font-black text-slate-900 group-hover:text-indigo-600 transition-colors">{student.name}</h5>
                       <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{student.module}</p>
                     </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-black text-slate-900">{student.progress}%</p>
                    <div className="w-24 h-1 bg-slate-100 rounded-full mt-1.5 overflow-hidden">
                       <div className="h-full bg-indigo-500" style={{width: `${student.progress}%`}}></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <button className="w-full mt-8 py-4 bg-slate-50 border border-slate-200 text-slate-500 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-100 hover:text-slate-900 transition-all">
               View Full Roster
            </button>
          </Card>
        </div>
      )}

      {activeTab === 'roster' && (
        <Card noPadding={true}>
          <div className="overflow-x-auto">
             <table className="w-full text-left">
                <thead className="bg-slate-50 border-b border-slate-200/60">
                   <tr>
                     <th className="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Student</th>
                     <th className="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Current Topic</th>
                     <th className="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Mastery Level</th>
                     <th className="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Engagement</th>
                     <th className="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Action</th>
                   </tr>
                </thead>
                <tbody className="divide-y divide-slate-100/60 font-medium text-sm text-slate-700">
                   {classList.map(s => (
                     <tr key={s.id} className="hover:bg-slate-50/50 transition-colors">
                       <td className="px-8 py-5 flex items-center space-x-3">
                         <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-black text-[10px] border border-indigo-100 italic">
                            LF
                         </div>
                         <span className="font-bold text-slate-900">{s.name}</span>
                       </td>
                       <td className="px-8 py-5">{s.module}</td>
                       <td className="px-8 py-5">
                          <Badge variant={s.mastery === 'proficient' ? 'success' : 'info'}>{s.mastery}</Badge>
                       </td>
                       <td className="px-8 py-5">
                          <div className="flex items-center space-x-3">
                             <div className="w-12 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                <div className="h-full bg-purple-500" style={{width: `${s.engagement}%`}}></div>
                             </div>
                             <span className="text-xs font-black text-slate-400">{s.engagement}%</span>
                          </div>
                       </td>
                       <td className="px-8 py-5">
                          <button className="text-[10px] font-black text-indigo-500 hover:text-indigo-700 uppercase tracking-widest transition-colors">Details ↗</button>
                       </td>
                     </tr>
                   ))}
                </tbody>
             </table>
          </div>
        </Card>
      )}

      {activeTab === 'alerts' && (
         <div className="max-w-3xl mx-auto space-y-6">
            {struggleAlerts.length === 0 ? (
              <div className="p-20 text-center space-y-4 bg-emerald-50 rounded-[3rem] border border-emerald-100">
                <span className="text-5xl">🧘</span>
                <h4 className="text-xl font-black text-emerald-900">All Calm</h4>
                <p className="text-emerald-700 font-medium">No active struggles detected. Everyone is making steady progress.</p>
              </div>
            ) : (
              struggleAlerts.map(a => (
                <Card key={a.id} className="relative overflow-hidden group">
                  <div className={`absolute top-0 left-0 bottom-0 w-2 ${a.severity === 'high' ? 'bg-rose-500' : 'bg-amber-500'}`}></div>
                  <div className="space-y-6">
                    <div className="flex justify-between items-center">
                       <div className="flex items-center space-x-4">
                          <div className="w-12 h-12 rounded-2xl bg-slate-50 flex items-center justify-center font-black text-xl text-slate-400 border border-slate-100">
                            {a.student.charAt(0)}
                          </div>
                          <div>
                            <h4 className="font-black text-slate-900">{a.student}</h4>
                            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest italic">{a.agentTriggered} Agent detected</p>
                          </div>
                       </div>
                       <div className="text-right">
                         <span className={`text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-full ${a.severity === 'high' ? 'bg-rose-100 text-rose-600' : 'bg-amber-100 text-amber-600'}`}>
                           {a.severity} Severity
                         </span>
                       </div>
                    </div>
                    
                    <div className="p-6 bg-slate-50 rounded-3xl space-y-4">
                       <h5 className="text-sm font-black text-slate-900 leading-relaxed group-hover:text-indigo-600 transition-colors">
                         "{a.issue}"
                       </h5>
                       <div className="space-y-2">
                          <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Detection Factors:</p>
                          <div className="flex flex-wrap gap-2">
                            {a.factors.map((f, i) => (
                              <span key={i} className="px-3 py-1 bg-white rounded-full text-[10px] font-bold text-slate-600 border border-slate-200">
                                {f}
                              </span>
                            ))}
                          </div>
                       </div>
                    </div>

                    <div className="flex gap-4">
                       <button className="flex-1 btn-premium">Intervene ↗</button>
                       <button className="px-8 py-4 bg-white border border-slate-200 rounded-2xl text-xs font-black text-slate-600 hover:bg-slate-50 transition-all uppercase tracking-widest">
                         Ignore
                       </button>
                    </div>
                  </div>
                </Card>
              ))
            )}
         </div>
      )}
    </div>
  );
};

export default TeacherDashboardView;