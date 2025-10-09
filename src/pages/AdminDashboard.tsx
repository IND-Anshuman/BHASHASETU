import { Home, Users, BookOpen, Languages, TrendingUp, Download, Settings, ChevronRight, BarChart3 } from 'lucide-react';
import { useState } from 'react';

type Page = 'landing' | 'learner' | 'admin' | 'translation' | 'voice';

interface AdminDashboardProps {
  onNavigate: (page: Page) => void;
}

export default function AdminDashboard({ onNavigate }: AdminDashboardProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'modules' | 'learners' | 'analytics'>('overview');

  const languageCoverage = [
    { language: 'Hindi', coverage: 95, color: 'from-blue-600 to-indigo-600' },
    { language: 'Tamil', coverage: 87, color: 'from-cyan-600 to-teal-600' },
    { language: 'Telugu', coverage: 82, color: 'from-green-600 to-emerald-600' },
    { language: 'Bengali', coverage: 78, color: 'from-violet-600 to-purple-600' },
    { language: 'Marathi', coverage: 72, color: 'from-sky-600 to-blue-600' },
    { language: 'Gujarati', coverage: 68, color: 'from-teal-600 to-cyan-600' },
  ];

  const modules = [
    { name: 'Welding Fundamentals', translations: 18, quality: 94, engagement: 4.7 },
    { name: 'Electrical Basics', translations: 15, quality: 91, engagement: 4.5 },
    { name: 'Carpentry Skills', translations: 20, quality: 88, engagement: 4.6 },
    { name: 'Plumbing Essentials', translations: 12, quality: 86, engagement: 4.4 },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-violet-50/30 to-purple-50/40">
      <nav className="bg-white/90 backdrop-blur-md border-b border-slate-200/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <button
              onClick={() => onNavigate('landing')}
              className="flex items-center space-x-2 text-slate-700 hover:text-violet-600 transition-colors"
            >
              <Home className="w-5 h-5" />
              <span className="font-medium">Home</span>
            </button>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => onNavigate('translation')}
                className="px-4 py-2 bg-gradient-to-r from-violet-600 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all text-sm font-medium"
              >
                Translation Tool
              </button>
              <button
                onClick={() => onNavigate('voice')}
                className="px-4 py-2 bg-white border-2 border-slate-200 text-slate-700 rounded-lg hover:border-violet-600 transition-all text-sm font-medium"
              >
                Voice Module
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">Admin Dashboard</h1>
          <p className="text-slate-600">Monitor and manage your multilingual training platform</p>
        </div>

        <div className="mb-6">
          <div className="flex space-x-2 bg-white/80 backdrop-blur-sm rounded-xl p-2 w-fit shadow-sm border border-slate-200/50">
            {['overview', 'modules', 'learners', 'analytics'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab as any)}
                className={`px-6 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === tab
                    ? 'bg-gradient-to-r from-violet-600 to-purple-600 text-white shadow-md'
                    : 'text-slate-600 hover:text-slate-800'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div className="grid md:grid-cols-4 gap-6">
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-100/50 shadow-lg">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center">
                    <Users className="w-6 h-6 text-white" />
                  </div>
                  <TrendingUp className="w-5 h-5 text-blue-600" />
                </div>
                <p className="text-3xl font-bold text-slate-800 mb-1">10,247</p>
                <p className="text-sm text-slate-600">Total Learners</p>
                <p className="text-xs text-blue-600 font-medium mt-2">+12% this month</p>
              </div>

              <div className="bg-gradient-to-br from-cyan-50 to-teal-50 rounded-2xl p-6 border border-cyan-100/50 shadow-lg">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-cyan-600 to-teal-600 rounded-xl flex items-center justify-center">
                    <BookOpen className="w-6 h-6 text-white" />
                  </div>
                  <TrendingUp className="w-5 h-5 text-cyan-600" />
                </div>
                <p className="text-3xl font-bold text-slate-800 mb-1">534</p>
                <p className="text-sm text-slate-600">Active Courses</p>
                <p className="text-xs text-cyan-600 font-medium mt-2">+8 new courses</p>
              </div>

              <div className="bg-gradient-to-br from-violet-50 to-purple-50 rounded-2xl p-6 border border-violet-100/50 shadow-lg">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-violet-600 to-purple-600 rounded-xl flex items-center justify-center">
                    <Languages className="w-6 h-6 text-white" />
                  </div>
                  <TrendingUp className="w-5 h-5 text-violet-600" />
                </div>
                <p className="text-3xl font-bold text-slate-800 mb-1">22</p>
                <p className="text-sm text-slate-600">Languages</p>
                <p className="text-xs text-violet-600 font-medium mt-2">82% avg coverage</p>
              </div>

              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-6 border border-green-100/50 shadow-lg">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-green-600 to-emerald-600 rounded-xl flex items-center justify-center">
                    <BarChart3 className="w-6 h-6 text-white" />
                  </div>
                  <TrendingUp className="w-5 h-5 text-green-600" />
                </div>
                <p className="text-3xl font-bold text-slate-800 mb-1">4.6</p>
                <p className="text-sm text-slate-600">Avg Engagement</p>
                <p className="text-xs text-green-600 font-medium mt-2">+0.3 improvement</p>
              </div>
            </div>

            <div className="grid lg:grid-cols-2 gap-6">
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-slate-800">Language Coverage</h3>
                  <button className="text-sm text-violet-600 hover:text-violet-700 font-medium flex items-center space-x-1">
                    <span>View All</span>
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
                <div className="space-y-4">
                  {languageCoverage.map((lang) => (
                    <div key={lang.language}>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="font-medium text-slate-700">{lang.language}</span>
                        <span className="text-slate-600">{lang.coverage}%</span>
                      </div>
                      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                        <div
                          className={`h-full bg-gradient-to-r ${lang.color} rounded-full transition-all duration-500`}
                          style={{ width: `${lang.coverage}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-slate-800">Translation Quality</h3>
                  <button className="px-4 py-2 bg-gradient-to-r from-violet-600 to-purple-600 text-white rounded-lg text-sm font-medium hover:shadow-lg transition-all">
                    <Download className="w-4 h-4 inline mr-2" />
                    Export
                  </button>
                </div>
                <div className="space-y-4">
                  {modules.map((module, index) => (
                    <div key={index} className="bg-gradient-to-br from-slate-50 to-violet-50/30 rounded-xl p-4 border border-slate-200/50">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-semibold text-slate-800">{module.name}</h4>
                        <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
                          {module.quality}% quality
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <p className="text-slate-600">Translations</p>
                          <p className="font-semibold text-slate-800">{module.translations} languages</p>
                        </div>
                        <div>
                          <p className="text-slate-600">Engagement</p>
                          <p className="font-semibold text-slate-800">{module.engagement}/5.0</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4">Learner Engagement Metrics</h3>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="w-24 h-24 mx-auto mb-3 relative">
                    <svg className="w-full h-full transform -rotate-90">
                      <circle
                        cx="48"
                        cy="48"
                        r="40"
                        stroke="#e2e8f0"
                        strokeWidth="8"
                        fill="none"
                      />
                      <circle
                        cx="48"
                        cy="48"
                        r="40"
                        stroke="url(#gradient1)"
                        strokeWidth="8"
                        fill="none"
                        strokeDasharray={`${2 * Math.PI * 40}`}
                        strokeDashoffset={`${2 * Math.PI * 40 * (1 - 0.73)}`}
                        strokeLinecap="round"
                      />
                      <defs>
                        <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="0%">
                          <stop offset="0%" stopColor="#3b82f6" />
                          <stop offset="100%" stopColor="#6366f1" />
                        </linearGradient>
                      </defs>
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-2xl font-bold text-slate-800">73%</span>
                    </div>
                  </div>
                  <p className="font-medium text-slate-800">Completion Rate</p>
                  <p className="text-sm text-slate-600 mt-1">Avg across all courses</p>
                </div>

                <div className="text-center">
                  <div className="w-24 h-24 mx-auto mb-3 relative">
                    <svg className="w-full h-full transform -rotate-90">
                      <circle
                        cx="48"
                        cy="48"
                        r="40"
                        stroke="#e2e8f0"
                        strokeWidth="8"
                        fill="none"
                      />
                      <circle
                        cx="48"
                        cy="48"
                        r="40"
                        stroke="url(#gradient2)"
                        strokeWidth="8"
                        fill="none"
                        strokeDasharray={`${2 * Math.PI * 40}`}
                        strokeDashoffset={`${2 * Math.PI * 40 * (1 - 0.85)}`}
                        strokeLinecap="round"
                      />
                      <defs>
                        <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="0%">
                          <stop offset="0%" stopColor="#06b6d4" />
                          <stop offset="100%" stopColor="#14b8a6" />
                        </linearGradient>
                      </defs>
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-2xl font-bold text-slate-800">85%</span>
                    </div>
                  </div>
                  <p className="font-medium text-slate-800">Satisfaction</p>
                  <p className="text-sm text-slate-600 mt-1">Based on feedback</p>
                </div>

                <div className="text-center">
                  <div className="w-24 h-24 mx-auto mb-3 relative">
                    <svg className="w-full h-full transform -rotate-90">
                      <circle
                        cx="48"
                        cy="48"
                        r="40"
                        stroke="#e2e8f0"
                        strokeWidth="8"
                        fill="none"
                      />
                      <circle
                        cx="48"
                        cy="48"
                        r="40"
                        stroke="url(#gradient3)"
                        strokeWidth="8"
                        fill="none"
                        strokeDasharray={`${2 * Math.PI * 40}`}
                        strokeDashoffset={`${2 * Math.PI * 40 * (1 - 0.68)}`}
                        strokeLinecap="round"
                      />
                      <defs>
                        <linearGradient id="gradient3" x1="0%" y1="0%" x2="100%" y2="0%">
                          <stop offset="0%" stopColor="#7c3aed" />
                          <stop offset="100%" stopColor="#a855f7" />
                        </linearGradient>
                      </defs>
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-2xl font-bold text-slate-800">68%</span>
                    </div>
                  </div>
                  <p className="font-medium text-slate-800">Active Users</p>
                  <p className="text-sm text-slate-600 mt-1">Weekly engagement</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab !== 'overview' && (
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-12 text-center">
            <Settings className="w-16 h-16 text-slate-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-slate-800 mb-2">
              {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Section
            </h3>
            <p className="text-slate-600">This section is being developed with detailed analytics and management tools.</p>
          </div>
        )}
      </div>
    </div>
  );
}
