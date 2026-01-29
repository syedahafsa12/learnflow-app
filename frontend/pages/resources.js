import React, { useState } from 'react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

const ResourcesView = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const resources = [
    { title: 'Python Fundamentals', category: 'tutorial', level: 'beginner', duration: '30 min', downloads: 156, icon: '📖' },
    { title: 'Control Flow Patterns', category: 'tutorial', level: 'intermediate', duration: '45 min', downloads: 89, icon: '🔄' },
    { title: 'Data Structures', category: 'tutorial', level: 'intermediate', duration: '60 min', downloads: 201, icon: '📦' },
    { title: 'Cheat Sheet 2024', category: 'reference', level: 'all', duration: '5 min', downloads: 512, icon: '📑' },
    { title: 'Debugging Pro-Tips', category: 'guide', level: 'intermediate', duration: '25 min', downloads: 76, icon: '🐛' },
  ];

  return (
    <div className="space-y-10 pb-12 animate-in fade-in duration-700">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-sky-50 text-sky-700 rounded-full text-[10px] font-black uppercase tracking-widest ring-1 ring-sky-200">
            Self-Service Library
          </div>
          <h1 className="text-4xl font-black tracking-tight text-slate-900">Learning Resources</h1>
          <p className="text-slate-500 font-medium">Curated high-quality assets for your technical growth.</p>
        </div>
        
        <div className="max-w-md w-full">
           <div className="relative group">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search tutorials, cheat sheets..."
                className="w-full pl-12 pr-6 py-4 bg-white border border-slate-200 rounded-2xl shadow-sm focus:outline-none focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 transition-all font-medium text-slate-900 placeholder-slate-400"
              />
              <span className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400 text-lg group-focus-within:text-sky-500 transition-colors">🔍</span>
           </div>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3">
         {['all', 'tutorial', 'reference', 'guide'].map(cat => (
           <button
             key={cat}
             onClick={() => setSelectedCategory(cat)}
             className={`px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${
               selectedCategory === cat ? 'bg-slate-900 text-white shadow-xl shadow-slate-900/20' : 'bg-white text-slate-500 hover:text-slate-900 border border-slate-100'
             }`}
           >
             {cat === 'all' ? 'All Classes' : cat}
           </button>
         ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {resources.filter(r => selectedCategory === 'all' || r.category === selectedCategory).map((res, i) => (
          <Card key={i} className="group relative overflow-hidden transition-all duration-500 hover:-translate-y-2">
            <div className="absolute top-0 right-0 p-6 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
               <span className="text-2xl cursor-pointer hover:scale-125 transition-transform block">⭐</span>
            </div>
            
            <div className="space-y-6">
               <div className="w-16 h-16 rounded-[1.5rem] bg-slate-50 flex items-center justify-center text-3xl group-hover:bg-indigo-600 group-hover:text-white transition-all duration-500 shadow-inner">
                 {res.icon}
               </div>

               <div className="space-y-2">
                 <div className="flex items-center space-x-2">
                    <Badge variant={res.level === 'beginner' ? 'success' : 'warning'} size="sm">{res.level}</Badge>
                    <span className="text-[10px] font-black text-slate-300 uppercase leading-none">•</span>
                    <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{res.duration}</span>
                 </div>
                 <h3 className="text-xl font-black text-slate-900 tracking-tight leading-tight group-hover:text-indigo-600 transition-colors">
                   {res.title}
                 </h3>
                 <p className="text-sm text-slate-500 font-medium leading-relaxed">
                   Comprehensive guide by AI agents to master {res.title.toLowerCase()}.
                 </p>
               </div>

               <div className="pt-6 border-t border-slate-100 flex items-center justify-between">
                  <div>
                    <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Impact</p>
                    <p className="text-sm font-black text-slate-900">High Score Potential</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs font-black text-indigo-500">{res.downloads}</p>
                    <p className="text-[8px] font-black text-slate-400 uppercase tracking-widest">Readers</p>
                  </div>
               </div>

               <div className="flex gap-4">
                  <button className="flex-1 py-4 bg-indigo-50 hover:bg-indigo-600 hover:text-white text-indigo-600 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all duration-300">Preview</button>
                  <button className="flex-1 btn-premium px-0">Unlock ↗</button>
               </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default ResourcesView;