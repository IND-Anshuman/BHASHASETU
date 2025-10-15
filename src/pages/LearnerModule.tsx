import { Home, ChevronLeft, ChevronRight, Volume2, BookOpen, CheckCircle, Circle, Languages, LogOut, User, Loader2 } from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

type Page = 'landing' | 'learner' | 'admin' | 'translation' | 'voice';

interface LearnerModuleProps {
  onNavigate: (page: Page) => void;
}

export default function LearnerModule({ onNavigate }: LearnerModuleProps) {
  const { user, loading, signOut } = useAuth();
  const [isDualLanguage, setIsDualLanguage] = useState(true);
  const [selectedLanguage, setSelectedLanguage] = useState('Hindi');
  const [currentLesson, setCurrentLesson] = useState(0);

  const lessons = [
    { id: 1, title: 'Introduction to Welding', completed: true },
    { id: 2, title: 'Safety Equipment & Procedures', completed: true },
    { id: 3, title: 'Types of Welding Joints', completed: false },
    { id: 4, title: 'Arc Welding Basics', completed: false },
    { id: 5, title: 'Practical Exercise 1', completed: false },
  ];

  const content = {
    english: {
      title: 'Types of Welding Joints',
      content: 'Welding joints are classified based on how the metal pieces are positioned relative to each other. The five basic types of joints are: butt joint, corner joint, edge joint, lap joint, and T-joint. Each type serves specific applications and requires different welding techniques.'
    },
    hindi: {
      title: 'वेल्डिंग जोड़ों के प्रकार',
      content: 'वेल्डिंग जोड़ों को धातु के टुकड़ों की एक-दूसरे के सापेक्ष स्थिति के आधार पर वर्गीकृत किया जाता है। पांच बुनियादी प्रकार के जोड़ हैं: बट जॉइंट, कॉर्नर जॉइंट, एज जॉइंट, लैप जॉइंट, और टी-जॉइंट। प्रत्येक प्रकार विशिष्ट अनुप्रयोगों के लिए उपयोग किया जाता है और विभिन्न वेल्डिंग तकनीकों की आवश्यकता होती है।'
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-cyan-50/30 to-teal-50/40">
      <nav className="bg-white/90 backdrop-blur-md border-b border-slate-200/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <button
              onClick={() => onNavigate('landing')}
              className="flex items-center space-x-2 text-slate-700 hover:text-cyan-600 transition-colors"
            >
              <Home className="w-5 h-5" />
              <span className="font-medium">Home</span>
            </button>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 bg-gradient-to-r from-cyan-100 to-teal-100 px-4 py-2 rounded-full">
                <BookOpen className="w-4 h-4 text-cyan-600" />
                <span className="text-sm font-medium text-slate-700">Welding Fundamentals</span>
              </div>
              {/* Auth controls */}
              {loading ? (
                <div className="flex items-center justify-center p-2">
                  <Loader2 className="w-5 h-5 animate-spin text-cyan-600" />
                </div>
              ) : user ? (
                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-gradient-to-r from-cyan-600 to-teal-600 rounded-full flex items-center justify-center">
                      {user.user_metadata?.avatar_url ? (
                        <img
                          src={user.user_metadata.avatar_url}
                          alt="Profile"
                          className="w-8 h-8 rounded-full object-cover"
                        />
                      ) : (
                        <User className="w-4 h-4 text-white" />
                      )}
                    </div>
                    <div className="text-sm">
                      <p className="font-medium text-slate-800">
                        {user.user_metadata?.full_name || user.email?.split('@')[0]}
                      </p>
                      <p className="text-xs text-slate-600">Google Account</p>
                    </div>
                  </div>
                  <button
                    onClick={signOut}
                    className="flex items-center space-x-1 px-3 py-1.5 text-sm text-slate-600 hover:text-red-600 transition-colors rounded-lg hover:bg-red-50"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Logout</span>
                  </button>
                </div>
              ) : (
                <div className="text-sm font-medium text-slate-700">
                  Welcome, Guest
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-4 gap-6">
          <div className="lg:col-span-1">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6 sticky top-24">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center space-x-2">
                <BookOpen className="w-5 h-5 text-cyan-600" />
                <span>Course Modules</span>
              </h3>
              <div className="space-y-2">
                {lessons.map((lesson, index) => (
                  <button
                    key={lesson.id}
                    onClick={() => setCurrentLesson(index)}
                    className={`w-full text-left px-4 py-3 rounded-xl transition-all flex items-center space-x-3 ${
                      currentLesson === index
                        ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-lg'
                        : 'bg-slate-50 text-slate-700 hover:bg-slate-100'
                    }`}
                  >
                    {lesson.completed ? (
                      <CheckCircle className="w-4 h-4 flex-shrink-0" />
                    ) : (
                      <Circle className="w-4 h-4 flex-shrink-0" />
                    )}
                    <span className="text-sm font-medium flex-1">{lesson.title}</span>
                  </button>
                ))}
              </div>

              <div className="mt-6 pt-6 border-t border-slate-200">
                <div className="mb-3">
                  <div className="flex justify-between text-sm text-slate-600 mb-2">
                    <span>Progress</span>
                    <span className="font-semibold">40%</span>
                  </div>
                  <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                    <div className="h-full w-2/5 bg-gradient-to-r from-cyan-600 to-teal-600 rounded-full"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="lg:col-span-3 space-y-6">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
                <h2 className="text-2xl font-bold text-slate-800">
                  {isDualLanguage ? 'Lesson 3: Dual-Language View' : content.english.title}
                </h2>
                <div className="flex items-center space-x-3">
                  <button
                    onClick={() => setIsDualLanguage(!isDualLanguage)}
                    className={`px-4 py-2 rounded-lg transition-all flex items-center space-x-2 ${
                      isDualLanguage
                        ? 'bg-gradient-to-r from-cyan-600 to-teal-600 text-white shadow-md'
                        : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                    }`}
                  >
                    <Languages className="w-4 h-4" />
                    <span className="text-sm font-medium">Dual Language</span>
                  </button>
                  <select
                    value={selectedLanguage}
                    onChange={(e) => setSelectedLanguage(e.target.value)}
                    className="px-4 py-2 bg-slate-100 rounded-lg text-sm font-medium text-slate-700 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  >
                    <option>Hindi</option>
                    <option>Tamil</option>
                    <option>Telugu</option>
                    <option>Bengali</option>
                    <option>Marathi</option>
                    <option>Gujarati</option>
                  </select>
                </div>
              </div>

              {isDualLanguage ? (
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="flex items-center space-x-2 mb-3">
                      <div className="w-1 h-6 bg-gradient-to-b from-slate-600 to-slate-700 rounded-full"></div>
                      <h3 className="text-lg font-semibold text-slate-800">English</h3>
                    </div>
                    <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-xl p-6 border border-slate-200/50">
                      <h4 className="font-semibold text-slate-800 mb-3">{content.english.title}</h4>
                      <p className="text-slate-700 leading-relaxed">{content.english.content}</p>
                      <button className="mt-4 flex items-center space-x-2 text-slate-600 hover:text-slate-700 transition-colors">
                        <Volume2 className="w-4 h-4" />
                        <span className="text-sm font-medium">Listen</span>
                      </button>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center space-x-2 mb-3">
                      <div className="w-1 h-6 bg-gradient-to-b from-cyan-600 to-teal-600 rounded-full"></div>
                      <h3 className="text-lg font-semibold text-slate-800">{selectedLanguage}</h3>
                    </div>
                    <div className="bg-gradient-to-br from-cyan-50 to-teal-50 rounded-xl p-6 border border-cyan-100/50">
                      <h4 className="font-semibold text-slate-800 mb-3">{content.hindi.title}</h4>
                      <p className="text-slate-700 leading-relaxed">{content.hindi.content}</p>
                      <button className="mt-4 flex items-center space-x-2 text-cyan-600 hover:text-cyan-700 transition-colors">
                        <Volume2 className="w-4 h-4" />
                        <span className="text-sm font-medium">सुनें</span>
                      </button>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="bg-gradient-to-br from-slate-50 to-cyan-50 rounded-xl p-6 border border-slate-200/50">
                    <h4 className="font-semibold text-slate-800 mb-3">{content.english.title}</h4>
                    <p className="text-slate-700 leading-relaxed">{content.english.content}</p>
                    <button className="mt-4 flex items-center space-x-2 text-slate-600 hover:text-slate-700 transition-colors">
                      <Volume2 className="w-4 h-4" />
                      <span className="text-sm font-medium">Listen</span>
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4">Visual Guide</h3>
              <div className="aspect-video bg-gradient-to-br from-slate-100 to-cyan-100 rounded-xl flex items-center justify-center relative overflow-hidden border border-slate-200/50">
                <div className="absolute inset-0 bg-gradient-to-br from-cyan-400/10 to-teal-400/10"></div>
                <div className="relative text-center p-8">
                  <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
                    <Volume2 className="w-10 h-10 text-cyan-600" />
                  </div>
                  <p className="text-slate-600 font-medium">Video with subtitles in {selectedLanguage}</p>
                </div>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <button className="flex items-center space-x-2 px-6 py-3 bg-white rounded-xl border-2 border-slate-200 text-slate-700 hover:border-cyan-600 transition-all shadow-sm">
                <ChevronLeft className="w-5 h-5" />
                <span className="font-medium">Previous</span>
              </button>
              <button className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-cyan-600 to-teal-600 text-white rounded-xl hover:shadow-xl transition-all">
                <span className="font-medium">Next Lesson</span>
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
