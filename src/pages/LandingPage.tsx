import { Globe2, Languages, Mic, BookOpen, Users, ArrowRight, Menu, X } from 'lucide-react';
import { useState } from 'react';
import GoogleLogin from '../components/GoogleLogin';

type Page = 'landing' | 'learner' | 'admin' | 'translation' | 'voice';

interface LandingPageProps {
  onNavigate: (page: Page) => void;
}

export default function LandingPage({ onNavigate }: LandingPageProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/40">
      <nav className="fixed w-full bg-white/80 backdrop-blur-md z-50 border-b border-slate-200/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Globe2 className="w-8 h-8 text-blue-600" />
              <span className="text-2xl font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                BhashaSetu
              </span>
            </div>

            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-slate-700 hover:text-blue-600 transition-colors">Features</a>
              <a href="#about" className="text-slate-700 hover:text-blue-600 transition-colors">About</a>
              <a href="#contact" className="text-slate-700 hover:text-blue-600 transition-colors">Contact</a>
              <GoogleLogin />
              <button
                onClick={() => onNavigate('learner')}
                className="px-5 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full hover:shadow-lg transition-all"
              >
                Try Demo
              </button>
            </div>

            <button
              className="md:hidden text-slate-700"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div className="md:hidden bg-white border-t border-slate-200">
            <div className="px-4 py-4 space-y-3">
              <a href="#features" className="block text-slate-700 hover:text-blue-600">Features</a>
              <a href="#about" className="block text-slate-700 hover:text-blue-600">About</a>
              <a href="#contact" className="block text-slate-700 hover:text-blue-600">Contact</a>
              <div className="flex justify-center">
                <GoogleLogin />
              </div>
              <button
                onClick={() => onNavigate('learner')}
                className="w-full px-5 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full"
              >
                Try Demo
              </button>
            </div>
          </div>
        )}
      </nav>

      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <h1 className="text-5xl md:text-6xl font-bold text-slate-800 leading-tight">
                Breaking Language{' '}
                <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  Barriers
                </span>
              </h1>
              <p className="text-xl text-slate-600 leading-relaxed">
                Empowering vocational learners across India with AI-driven multilingual training.
                Learn in your language, master your craft.
              </p>
              <div className="flex flex-wrap gap-4">
                <button
                  onClick={() => onNavigate('learner')}
                  className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full hover:shadow-xl transition-all flex items-center space-x-2 group"
                >
                  <span>Try Demo</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </button>
                <button className="px-8 py-4 bg-white text-slate-700 rounded-full border-2 border-slate-200 hover:border-blue-600 transition-all">
                  Learn More
                </button>
              </div>
              <div className="mt-6">
                <p className="text-sm text-slate-600 mb-3">Or sign in to start learning:</p>
                <GoogleLogin />
              </div>
            </div>

            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-400/20 to-indigo-400/20 rounded-3xl blur-3xl"></div>
              <div className="relative bg-white/60 backdrop-blur-sm rounded-3xl p-8 shadow-xl border border-white/50">
                <div className="grid grid-cols-2 gap-4">
                  <div className="aspect-square bg-gradient-to-br from-blue-100 to-indigo-100 rounded-2xl p-6 flex flex-col items-center justify-center space-y-2">
                    <Languages className="w-12 h-12 text-blue-600" />
                    <span className="text-sm font-medium text-slate-700">22+ Languages</span>
                  </div>
                  <div className="aspect-square bg-gradient-to-br from-cyan-100 to-teal-100 rounded-2xl p-6 flex flex-col items-center justify-center space-y-2">
                    <Users className="w-12 h-12 text-cyan-600" />
                    <span className="text-sm font-medium text-slate-700">10K+ Learners</span>
                  </div>
                  <div className="aspect-square bg-gradient-to-br from-green-100 to-emerald-100 rounded-2xl p-6 flex flex-col items-center justify-center space-y-2">
                    <BookOpen className="w-12 h-12 text-green-600" />
                    <span className="text-sm font-medium text-slate-700">500+ Courses</span>
                  </div>
                  <div className="aspect-square bg-gradient-to-br from-purple-100 to-pink-100 rounded-2xl p-6 flex flex-col items-center justify-center space-y-2">
                    <Mic className="w-12 h-12 text-purple-600" />
                    <span className="text-sm font-medium text-slate-700">Voice Enabled</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="py-20 px-4 bg-white/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-slate-800 mb-4">Powerful Features</h2>
            <p className="text-xl text-slate-600">Everything you need for inclusive, accessible learning</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8 hover:shadow-xl transition-all border border-blue-100/50">
              <div className="w-14 h-14 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center mb-4">
                <Languages className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-3">Multilingual Translation</h3>
              <p className="text-slate-600">
                AI-powered translation across 22+ Indian languages with technical glossary support.
              </p>
            </div>

            <div className="bg-gradient-to-br from-cyan-50 to-teal-50 rounded-2xl p-8 hover:shadow-xl transition-all border border-cyan-100/50">
              <div className="w-14 h-14 bg-gradient-to-br from-cyan-600 to-teal-600 rounded-xl flex items-center justify-center mb-4">
                <BookOpen className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-3">Dual-Language Mode</h3>
              <p className="text-slate-600">
                Learn with side-by-side content in your native language and the source material.
              </p>
            </div>

            <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-8 hover:shadow-xl transition-all border border-green-100/50">
              <div className="w-14 h-14 bg-gradient-to-br from-green-600 to-emerald-600 rounded-xl flex items-center justify-center mb-4">
                <Globe2 className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-3">Regional Adaptation</h3>
              <p className="text-slate-600">
                Context-aware translations that respect regional dialects and cultural nuances.
              </p>
            </div>

            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-8 hover:shadow-xl transition-all border border-purple-100/50">
              <div className="w-14 h-14 bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl flex items-center justify-center mb-4">
                <Mic className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-3">Speech Accessibility</h3>
              <p className="text-slate-600">
                Text-to-speech and subtitle generation for audio-visual learning experiences.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-slate-800 mb-6">Ready to Get Started?</h2>
          <p className="text-xl text-slate-600 mb-8">
            Join thousands of learners breaking language barriers every day
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <button
              onClick={() => onNavigate('learner')}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full hover:shadow-xl transition-all"
            >
              Try Demo
            </button>
            <button
              onClick={() => onNavigate('admin')}
              className="px-8 py-4 bg-white text-slate-700 rounded-full border-2 border-slate-200 hover:border-blue-600 transition-all"
            >
              View Dashboard
            </button>
          </div>
        </div>
      </section>

      <footer className="bg-slate-900 text-slate-300 py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Globe2 className="w-6 h-6 text-blue-500" />
                <span className="text-xl font-semibold text-white">BhashaSetu</span>
              </div>
              <p className="text-sm">
                Empowering vocational education through multilingual accessibility.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#features" className="hover:text-blue-500 transition-colors">Features</a></li>
                <li><button onClick={() => onNavigate('learner')} className="hover:text-blue-500 transition-colors">Demo</button></li>
                <li><a href="#pricing" className="hover:text-blue-500 transition-colors">Pricing</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#about" className="hover:text-blue-500 transition-colors">About</a></li>
                <li><a href="#contact" className="hover:text-blue-500 transition-colors">Contact</a></li>
                <li><a href="#privacy" className="hover:text-blue-500 transition-colors">Privacy Policy</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Connect</h4>
              <div className="flex space-x-4">
                <a href="#" className="hover:text-blue-500 transition-colors">Twitter</a>
                <a href="#" className="hover:text-blue-500 transition-colors">LinkedIn</a>
                <a href="#" className="hover:text-blue-500 transition-colors">GitHub</a>
              </div>
            </div>
          </div>
          <div className="border-t border-slate-800 pt-8 text-center text-sm">
            <p>&copy; 2025 BhashaSetu. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
