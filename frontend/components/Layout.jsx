import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useUser } from '../context/UserContext';

const Layout = ({ children }) => {
  const { user, toggleRole } = useUser();
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navigation = [
    { name: 'Dashboard', href: '/', icon: '🏠' },
    { name: 'AI Tutor', href: '/chat', icon: '🤖' },
    { name: 'Code Lab', href: '/editor', icon: '💻' },
    { name: 'Quiz Master', href: '/quiz', icon: '🧠' },
    { name: 'Progress', href: '/progress', icon: '📊' },
    ...(user?.role === 'teacher' ? [{ name: 'Teacher Hub', href: '/teacher', icon: '👨‍🏫' }] : []),
    { name: 'Resources', href: '/resources', icon: '📚' }
  ];

  const isActive = (href) => router.pathname === href;

  return (
    <div className="min-h-screen text-slate-900" style={{background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)'}}>
      {/* Mobile sidebar */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div
            className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm"
            onClick={() => setSidebarOpen(false)}
          ></div>
          <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white shadow-xl">
            <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
              <nav className="mt-5 px-2 space-y-1">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`${
                      isActive(item.href)
                        ? 'bg-indigo-50 text-indigo-700'
                        : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                    } group flex items-center px-3 py-2 text-base font-medium rounded-xl transition-all duration-200`}
                  >
                    <span className="mr-4 text-xl">{item.icon}</span>
                    {item.name}
                  </Link>
                ))}
              </nav>
            </div>
          </div>
        </div>
      )}

      {/* Static sidebar for desktop */}
      <div className="hidden lg:flex lg:w-64 lg:flex-col lg:fixed lg:inset-y-0 shadow-sm">
        <div className="flex-1 flex flex-col min-h-0 bg-white border-r border-slate-200/60">
          <div className="flex-1 flex flex-col pt-8 pb-4 overflow-y-auto">
            <div className="flex items-center px-6 mb-8">
              <div className="text-2xl font-black tracking-tight" style={{background: 'linear-gradient(to right, #4f46e5, #9333ea)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'}}>
                LearnFlow
              </div>
              <div className="ml-2 px-1.5 py-0.5 bg-indigo-100 text-indigo-700 text-[10px] font-bold rounded uppercase tracking-wider">v2.0</div>
            </div>
            <nav className="flex-1 px-3 space-y-1">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`${
                    isActive(item.href)
                      ? 'bg-indigo-50 text-indigo-700 font-semibold'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  } group flex items-center px-3 py-2.5 text-sm font-medium rounded-xl transition-all duration-200`}
                >
                  <span className={`mr-3 text-lg transition-transform duration-200 ${isActive(item.href) ? 'scale-110' : 'group-hover:scale-110'}`}>{item.icon}</span>
                  {item.name}
                </Link>
              ))}
            </nav>
          </div>
          <div className="flex-shrink-0 p-4 border-t border-slate-100 bg-slate-50/50">
            <div className="bg-white p-3 rounded-2xl shadow-sm border border-slate-200/60">
              <div className="flex items-center mb-3">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center text-white text-lg font-bold shadow-md ring-2 ring-white" style={{background: 'linear-gradient(135deg, #6366f1, #a855f7)'}}>
                  {user?.name?.charAt(0) || 'U'}
                </div>
                <div className="ml-3 overflow-hidden">
                  <p className="text-sm font-bold text-slate-900 truncate">{user?.name || 'User'}</p>
                  <div className="flex items-center">
                    <span className={`w-1.5 h-1.5 rounded-full mr-1.5 ${user?.role === 'teacher' ? 'bg-purple-500' : 'bg-indigo-500'}`}></span>
                    <p className="text-[10px] text-slate-500 uppercase font-black tracking-widest">{user?.role || 'student'}</p>
                  </div>
                </div>
              </div>
              <button
                onClick={toggleRole}
                className="w-full py-2 px-4 bg-slate-900 text-white text-xs font-bold rounded-xl hover:bg-slate-800 transition-all duration-200 flex items-center justify-center space-x-2 shadow-sm"
              >
                <span>🔄</span>
                <span>Switch to {user?.role === 'student' ? 'Teacher' : 'Student'}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      {/* Main content */}
      <div className="lg:pl-64 flex flex-col flex-1">
        <header className="bg-white/70 backdrop-blur-md border-b border-slate-200/60 sticky top-0 z-30">
          <div className="px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-20">
              <button
                type="button"
                className="lg:hidden inline-flex items-center justify-center p-2.5 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 focus:outline-none transition-colors"
                onClick={() => setSidebarOpen(true)}
              >
                <span className="sr-only">Open sidebar</span>
                <span className="text-2xl">☰</span>
              </button>

              <div className="flex-1 flex justify-center lg:ml-6 lg:justify-end">
                <div className="max-w-md w-full">
                  <label htmlFor="search" className="sr-only">Search</label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                      <span className="text-slate-400">🔍</span>
                    </div>
                    <input
                      id="search"
                      name="search"
                      className="block w-full pl-11 pr-4 py-2.5 border-0 rounded-2xl bg-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:bg-white transition-all sm:text-sm"
                      placeholder="Search for lessons, quizzes, resources..."
                      type="search"
                    />
                  </div>
                </div>
              </div>

              <div className="ml-4 flex items-center md:ml-6 space-x-4">
                <button className="p-2 text-slate-400 hover:text-slate-900 transition-colors relative">
                  <span className="text-xl">🔔</span>
                  <span className="absolute top-2 right-2 block h-2 w-2 rounded-full bg-indigo-500 ring-2 ring-white"></span>
                </button>
                <div className="h-8 w-[1px] bg-slate-200 mx-2"></div>
                <div className="flex items-center space-x-3">
                  <div className="text-right hidden sm:block">
                    <p className="text-sm font-bold text-slate-900">{user?.name || 'User'}</p>
                    <p className="text-[10px] font-black text-indigo-500 uppercase tracking-widest">{user?.role || 'student'}</p>
                  </div>
                  <div className="w-10 h-10 rounded-full border-2 border-white shadow-sm ring-1 ring-slate-200 bg-slate-100 flex items-center justify-center font-bold text-slate-600">
                    {user?.name?.charAt(0) || 'U'}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </header>

        <main className="flex-1">
          <div className="py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;