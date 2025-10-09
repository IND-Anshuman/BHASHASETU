import { Home, Upload, Play, Pause, Volume2, Download, Languages, FileVideo, Activity, Settings } from 'lucide-react';
import { useState } from 'react';

type Page = 'landing' | 'learner' | 'admin' | 'translation' | 'voice';

interface VoiceModuleProps {
  onNavigate: (page: Page) => void;
}

export default function VoiceModule({ onNavigate }: VoiceModuleProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedVoiceLanguage, setSelectedVoiceLanguage] = useState('Hindi');
  const [subtitleLanguage, setSubtitleLanguage] = useState('Hindi');
  const [isDualSubtitles, setIsDualSubtitles] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [highContrast, setHighContrast] = useState(false);

  const handleGenerateAudio = () => {
    setIsProcessing(true);
    setTimeout(() => setIsProcessing(false), 3000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50/30 to-violet-50/40">
      <nav className="bg-white/90 backdrop-blur-md border-b border-slate-200/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <button
              onClick={() => onNavigate('admin')}
              className="flex items-center space-x-2 text-slate-700 hover:text-indigo-600 transition-colors"
            >
              <Home className="w-5 h-5" />
              <span className="font-medium">Dashboard</span>
            </button>
            <div className="flex items-center space-x-2">
              <div className="flex items-center space-x-2 bg-gradient-to-r from-indigo-100 to-violet-100 px-4 py-2 rounded-full">
                <Volume2 className="w-4 h-4 text-indigo-600" />
                <span className="text-sm font-medium text-slate-700">Voice & Subtitle Module</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">Voice & Subtitle Generation</h1>
          <p className="text-slate-600">Create multilingual audio and synchronized subtitles for your content</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-slate-800">Upload Media</h2>
                <button className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-violet-600 text-white rounded-lg hover:shadow-lg transition-all text-sm font-medium flex items-center space-x-2">
                  <Upload className="w-4 h-4" />
                  <span>Upload</span>
                </button>
              </div>

              <div className="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:border-indigo-500 transition-colors cursor-pointer bg-gradient-to-br from-slate-50 to-indigo-50/30">
                <FileVideo className="w-12 h-12 text-slate-400 mx-auto mb-3" />
                <p className="text-slate-700 font-medium mb-1">Drop video or audio files here</p>
                <p className="text-sm text-slate-500">Supports MP4, AVI, MP3, WAV formats</p>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-slate-800">Video Preview</h2>
                <div className="flex items-center space-x-2">
                  <select
                    value={subtitleLanguage}
                    onChange={(e) => setSubtitleLanguage(e.target.value)}
                    className="text-sm px-4 py-2 bg-slate-100 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-medium text-slate-700"
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

              <div className="aspect-video bg-gradient-to-br from-slate-900 to-indigo-900 rounded-xl overflow-hidden relative border border-slate-700/50 shadow-2xl">
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-white/10 backdrop-blur-sm rounded-full flex items-center justify-center mx-auto mb-4 border border-white/20">
                      <Play className="w-8 h-8 text-white ml-1" />
                    </div>
                    <p className="text-white/80 text-sm">Sample Training Video</p>
                    <p className="text-white/60 text-xs mt-1">Welding Safety Procedures</p>
                  </div>
                </div>

                <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-black/80 to-transparent">
                  {isDualSubtitles ? (
                    <div className="space-y-2 text-center">
                      <p
                        className={`text-base font-semibold ${
                          highContrast
                            ? 'bg-black text-white px-2 py-1 rounded inline-block'
                            : 'text-white drop-shadow-lg'
                        }`}
                        style={highContrast ? {} : { textShadow: '2px 2px 4px rgba(0,0,0,0.9)' }}
                      >
                        Always wear protective equipment when welding
                      </p>
                      <p
                        className={`text-base font-semibold ${
                          highContrast
                            ? 'bg-black text-yellow-300 px-2 py-1 rounded inline-block'
                            : 'text-yellow-300 drop-shadow-lg'
                        }`}
                        style={highContrast ? {} : { textShadow: '2px 2px 4px rgba(0,0,0,0.9)' }}
                      >
                        वेल्डिंग करते समय हमेशा सुरक्षा उपकरण पहनें
                      </p>
                    </div>
                  ) : (
                    <p
                      className={`text-base font-semibold text-center ${
                        highContrast
                          ? 'bg-black text-white px-2 py-1 rounded inline-block'
                          : 'text-white drop-shadow-lg'
                      }`}
                      style={highContrast ? {} : { textShadow: '2px 2px 4px rgba(0,0,0,0.9)' }}
                    >
                      वेल्डिंग करते समय हमेशा सुरक्षा उपकरण पहनें
                    </p>
                  )}
                </div>
              </div>

              <div className="mt-4 bg-gradient-to-r from-slate-50 to-indigo-50 rounded-xl p-4 border border-slate-200/50">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => setIsPlaying(!isPlaying)}
                      className="w-10 h-10 bg-gradient-to-r from-indigo-600 to-violet-600 rounded-full flex items-center justify-center text-white hover:shadow-lg transition-all"
                    >
                      {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-0.5" />}
                    </button>
                    <div className="flex-1">
                      <div className="h-1.5 bg-slate-200 rounded-full overflow-hidden">
                        <div className="h-full w-1/3 bg-gradient-to-r from-indigo-600 to-violet-600 rounded-full"></div>
                      </div>
                    </div>
                    <span className="text-sm font-medium text-slate-700">1:23 / 4:15</span>
                  </div>
                </div>

                <div className="flex items-center space-x-2 text-xs">
                  <Volume2 className="w-4 h-4 text-slate-600" />
                  <input type="range" min="0" max="100" defaultValue="70" className="flex-1 accent-indigo-600" />
                </div>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-slate-800">Audio Waveform</h2>
              </div>

              <div className="bg-gradient-to-br from-slate-50 to-indigo-50 rounded-xl p-6 border border-slate-200/50">
                <div className="flex items-end justify-center space-x-1 h-32">
                  {[...Array(50)].map((_, i) => {
                    const height = Math.random() * 100 + 20;
                    return (
                      <div
                        key={i}
                        className="flex-1 bg-gradient-to-t from-indigo-600 to-violet-600 rounded-full transition-all"
                        style={{ height: `${height}%`, maxWidth: '4px' }}
                      ></div>
                    );
                  })}
                </div>
                <div className="flex items-center justify-center mt-4 space-x-2 text-sm text-slate-600">
                  <Activity className="w-4 h-4" />
                  <span>Voice synthesis in progress</span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center space-x-2">
                <Settings className="w-5 h-5 text-indigo-600" />
                <span>Voice Settings</span>
              </h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Voice Language
                  </label>
                  <select
                    value={selectedVoiceLanguage}
                    onChange={(e) => setSelectedVoiceLanguage(e.target.value)}
                    className="w-full px-4 py-2.5 bg-slate-100 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-medium text-slate-700"
                  >
                    <option>Hindi</option>
                    <option>Tamil</option>
                    <option>Telugu</option>
                    <option>Bengali</option>
                    <option>Marathi</option>
                    <option>Gujarati</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Voice Type
                  </label>
                  <select className="w-full px-4 py-2.5 bg-slate-100 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-medium text-slate-700">
                    <option>Male (Natural)</option>
                    <option>Female (Natural)</option>
                    <option>Male (Professional)</option>
                    <option>Female (Professional)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Speech Rate
                  </label>
                  <input
                    type="range"
                    min="0.5"
                    max="2"
                    step="0.1"
                    defaultValue="1"
                    className="w-full accent-indigo-600"
                  />
                  <div className="flex justify-between text-xs text-slate-600 mt-1">
                    <span>0.5x</span>
                    <span>1.0x</span>
                    <span>2.0x</span>
                  </div>
                </div>

                <button
                  onClick={handleGenerateAudio}
                  disabled={isProcessing}
                  className="w-full px-4 py-3 bg-gradient-to-r from-indigo-600 to-violet-600 text-white rounded-lg hover:shadow-lg transition-all font-medium flex items-center justify-center space-x-2 disabled:opacity-50"
                >
                  {isProcessing ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Generating...</span>
                    </>
                  ) : (
                    <>
                      <Volume2 className="w-5 h-5" />
                      <span>Generate Audio</span>
                    </>
                  )}
                </button>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center space-x-2">
                <Languages className="w-5 h-5 text-indigo-600" />
                <span>Subtitle Options</span>
              </h3>

              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-gradient-to-br from-slate-50 to-indigo-50/30 rounded-xl border border-slate-200/50">
                  <div>
                    <p className="font-medium text-slate-800">Dual-Language</p>
                    <p className="text-xs text-slate-600 mt-1">Show both languages</p>
                  </div>
                  <button
                    onClick={() => setIsDualSubtitles(!isDualSubtitles)}
                    className={`w-12 h-6 rounded-full transition-all relative ${
                      isDualSubtitles ? 'bg-gradient-to-r from-indigo-600 to-violet-600' : 'bg-slate-300'
                    }`}
                  >
                    <div
                      className={`w-5 h-5 bg-white rounded-full absolute top-0.5 transition-all shadow-sm ${
                        isDualSubtitles ? 'right-0.5' : 'left-0.5'
                      }`}
                    ></div>
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 bg-gradient-to-br from-slate-50 to-indigo-50/30 rounded-xl border border-slate-200/50">
                  <div>
                    <p className="font-medium text-slate-800">High Contrast</p>
                    <p className="text-xs text-slate-600 mt-1">Enhanced readability</p>
                  </div>
                  <button
                    onClick={() => setHighContrast(!highContrast)}
                    className={`w-12 h-6 rounded-full transition-all relative ${
                      highContrast ? 'bg-gradient-to-r from-indigo-600 to-violet-600' : 'bg-slate-300'
                    }`}
                  >
                    <div
                      className={`w-5 h-5 bg-white rounded-full absolute top-0.5 transition-all shadow-sm ${
                        highContrast ? 'right-0.5' : 'left-0.5'
                      }`}
                    ></div>
                  </button>
                </div>

                <div className="p-4 bg-gradient-to-br from-slate-50 to-indigo-50/30 rounded-xl border border-slate-200/50">
                  <p className="font-medium text-slate-800 mb-2">Font Size</p>
                  <input
                    type="range"
                    min="12"
                    max="24"
                    defaultValue="16"
                    className="w-full accent-indigo-600"
                  />
                  <div className="flex justify-between text-xs text-slate-600 mt-1">
                    <span>Small</span>
                    <span>Medium</span>
                    <span>Large</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4">Export</h3>
              <div className="space-y-3">
                <button className="w-full px-4 py-3 bg-white border-2 border-slate-200 text-slate-700 rounded-lg hover:border-indigo-600 transition-all font-medium flex items-center justify-center space-x-2">
                  <Download className="w-5 h-5" />
                  <span>Download Audio</span>
                </button>
                <button className="w-full px-4 py-3 bg-white border-2 border-slate-200 text-slate-700 rounded-lg hover:border-indigo-600 transition-all font-medium flex items-center justify-center space-x-2">
                  <Download className="w-5 h-5" />
                  <span>Download Subtitles (SRT)</span>
                </button>
                <button className="w-full px-4 py-3 bg-gradient-to-r from-indigo-600 to-violet-600 text-white rounded-lg hover:shadow-lg transition-all font-medium flex items-center justify-center space-x-2">
                  <Download className="w-5 h-5" />
                  <span>Download Video</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
