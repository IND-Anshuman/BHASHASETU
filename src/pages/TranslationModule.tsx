import { Home, Upload, FileText, Languages, Settings, Plus, Trash2, Check, Sparkles, Download } from 'lucide-react';
import { useState } from 'react';

type Page = 'landing' | 'learner' | 'admin' | 'translation' | 'voice';

interface TranslationModuleProps {
  onNavigate: (page: Page) => void;
}

interface GlossaryTerm {
  term: string;
  translation: string;
}

export default function TranslationModule({ onNavigate }: TranslationModuleProps) {
  const [sourceLanguage, setSourceLanguage] = useState('English');
  const [targetLanguage, setTargetLanguage] = useState('Hindi');
  const [regionalAdaptation, setRegionalAdaptation] = useState(true);
  const [glossaryTerms, setGlossaryTerms] = useState<GlossaryTerm[]>([
    { term: 'Welding', translation: 'वेल्डिंग' },
    { term: 'Arc', translation: 'चाप' },
  ]);
  const [isTranslating, setIsTranslating] = useState(false);

  const sourceText = `Introduction to Welding Safety

Safety is the most critical aspect of welding operations. All welders must wear appropriate personal protective equipment (PPE) including welding helmets, gloves, and protective clothing. The welding area should be well-ventilated to prevent exposure to harmful fumes.

Key Safety Equipment:
• Welding helmet with proper shade lens
• Leather welding gloves
• Fire-resistant clothing
• Safety boots with steel toes`;

  const translatedText = `वेल्डिंग सुरक्षा का परिचय

वेल्डिंग संचालन में सुरक्षा सबसे महत्वपूर्ण पहलू है। सभी वेल्डरों को उचित व्यक्तिगत सुरक्षा उपकरण (पीपीई) पहनना चाहिए जिसमें वेल्डिंग हेलमेट, दस्ताने और सुरक्षात्मक कपड़े शामिल हैं। हानिकारक धुएं के संपर्क को रोकने के लिए वेल्डिंग क्षेत्र में अच्छा वेंटिलेशन होना चाहिए।

मुख्य सुरक्षा उपकरण:
• उचित शेड लेंस वाला वेल्डिंग हेलमेट
• चमड़े के वेल्डिंग दस्ताने
• आग प्रतिरोधी कपड़े
• स्टील के पंजों वाले सुरक्षा जूते`;

  const handleTranslate = () => {
    setIsTranslating(true);
    setTimeout(() => setIsTranslating(false), 2000);
  };

  const addGlossaryTerm = () => {
    setGlossaryTerms([...glossaryTerms, { term: '', translation: '' }]);
  };

  const removeGlossaryTerm = (index: number) => {
    setGlossaryTerms(glossaryTerms.filter((_, i) => i !== index));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-emerald-50/30 to-teal-50/40">
      <nav className="bg-white/90 backdrop-blur-md border-b border-slate-200/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <button
              onClick={() => onNavigate('admin')}
              className="flex items-center space-x-2 text-slate-700 hover:text-emerald-600 transition-colors"
            >
              <Home className="w-5 h-5" />
              <span className="font-medium">Dashboard</span>
            </button>
            <div className="flex items-center space-x-2">
              <div className="flex items-center space-x-2 bg-gradient-to-r from-emerald-100 to-teal-100 px-4 py-2 rounded-full">
                <Languages className="w-4 h-4 text-emerald-600" />
                <span className="text-sm font-medium text-slate-700">Translation Module</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">Content Translation</h1>
          <p className="text-slate-600">AI-powered translation with glossary management and regional adaptation</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-slate-800">Upload Content</h2>
                <button className="px-4 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-lg hover:shadow-lg transition-all text-sm font-medium flex items-center space-x-2">
                  <Upload className="w-4 h-4" />
                  <span>Upload File</span>
                </button>
              </div>

              <div className="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:border-emerald-500 transition-colors cursor-pointer bg-gradient-to-br from-slate-50 to-emerald-50/30">
                <FileText className="w-12 h-12 text-slate-400 mx-auto mb-3" />
                <p className="text-slate-700 font-medium mb-1">Drop files here or click to upload</p>
                <p className="text-sm text-slate-500">Supports PDF, DOCX, TXT, and video files</p>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-slate-800">Translation Preview</h2>
                <div className="flex items-center space-x-3">
                  <button
                    onClick={handleTranslate}
                    disabled={isTranslating}
                    className="px-6 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-lg hover:shadow-lg transition-all text-sm font-medium flex items-center space-x-2 disabled:opacity-50"
                  >
                    {isTranslating ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        <span>Translating...</span>
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4" />
                        <span>Translate</span>
                      </>
                    )}
                  </button>
                  <button className="px-4 py-2 bg-white border-2 border-slate-200 text-slate-700 rounded-lg hover:border-emerald-600 transition-all text-sm font-medium">
                    <Download className="w-4 h-4 inline mr-2" />
                    Export
                  </button>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-slate-800 flex items-center space-x-2">
                      <div className="w-1 h-5 bg-gradient-to-b from-blue-600 to-cyan-600 rounded-full"></div>
                      <span>Source ({sourceLanguage})</span>
                    </h3>
                    <select
                      value={sourceLanguage}
                      onChange={(e) => setSourceLanguage(e.target.value)}
                      className="text-sm px-3 py-1 bg-slate-100 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    >
                      <option>English</option>
                      <option>Hindi</option>
                      <option>Tamil</option>
                    </select>
                  </div>
                  <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-4 border border-blue-100/50 h-96 overflow-y-auto">
                    <pre className="text-sm text-slate-700 whitespace-pre-wrap font-sans leading-relaxed">
                      {sourceText}
                    </pre>
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-slate-800 flex items-center space-x-2">
                      <div className="w-1 h-5 bg-gradient-to-b from-emerald-600 to-teal-600 rounded-full"></div>
                      <span>Target ({targetLanguage})</span>
                    </h3>
                    <select
                      value={targetLanguage}
                      onChange={(e) => setTargetLanguage(e.target.value)}
                      className="text-sm px-3 py-1 bg-slate-100 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    >
                      <option>Hindi</option>
                      <option>Tamil</option>
                      <option>Telugu</option>
                      <option>Bengali</option>
                      <option>Marathi</option>
                      <option>Gujarati</option>
                    </select>
                  </div>
                  <div className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-xl p-4 border border-emerald-100/50 h-96 overflow-y-auto">
                    <pre className="text-sm text-slate-700 whitespace-pre-wrap font-sans leading-relaxed">
                      {translatedText}
                    </pre>
                  </div>
                </div>
              </div>

              <div className="mt-4 flex items-center justify-between bg-gradient-to-r from-emerald-50 to-teal-50 rounded-lg p-4 border border-emerald-100/50">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center">
                    <Check className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-800">Translation Quality: 94%</p>
                    <p className="text-sm text-slate-600">High confidence score with glossary adherence</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center space-x-2">
                <Settings className="w-5 h-5 text-emerald-600" />
                <span>Settings</span>
              </h3>

              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-gradient-to-br from-slate-50 to-emerald-50/30 rounded-xl border border-slate-200/50">
                  <div>
                    <p className="font-medium text-slate-800">Regional Adaptation</p>
                    <p className="text-xs text-slate-600 mt-1">Context-aware translations</p>
                  </div>
                  <button
                    onClick={() => setRegionalAdaptation(!regionalAdaptation)}
                    className={`w-12 h-6 rounded-full transition-all relative ${
                      regionalAdaptation ? 'bg-gradient-to-r from-emerald-600 to-teal-600' : 'bg-slate-300'
                    }`}
                  >
                    <div
                      className={`w-5 h-5 bg-white rounded-full absolute top-0.5 transition-all shadow-sm ${
                        regionalAdaptation ? 'right-0.5' : 'left-0.5'
                      }`}
                    ></div>
                  </button>
                </div>

                <div className="p-4 bg-gradient-to-br from-slate-50 to-emerald-50/30 rounded-xl border border-slate-200/50">
                  <p className="font-medium text-slate-800 mb-2">Quality Threshold</p>
                  <input
                    type="range"
                    min="70"
                    max="100"
                    defaultValue="90"
                    className="w-full accent-emerald-600"
                  />
                  <div className="flex justify-between text-xs text-slate-600 mt-1">
                    <span>70%</span>
                    <span>90%</span>
                    <span>100%</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800">Technical Glossary</h3>
                <button
                  onClick={addGlossaryTerm}
                  className="p-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-lg hover:shadow-lg transition-all"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>

              <div className="space-y-3 max-h-96 overflow-y-auto">
                {glossaryTerms.map((term, index) => (
                  <div
                    key={index}
                    className="flex items-center space-x-2 p-3 bg-gradient-to-br from-slate-50 to-emerald-50/30 rounded-xl border border-slate-200/50"
                  >
                    <div className="flex-1 space-y-2">
                      <input
                        type="text"
                        value={term.term}
                        placeholder="Term"
                        className="w-full px-3 py-1.5 bg-white rounded-lg text-sm border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                        onChange={(e) => {
                          const newTerms = [...glossaryTerms];
                          newTerms[index].term = e.target.value;
                          setGlossaryTerms(newTerms);
                        }}
                      />
                      <input
                        type="text"
                        value={term.translation}
                        placeholder="Translation"
                        className="w-full px-3 py-1.5 bg-white rounded-lg text-sm border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                        onChange={(e) => {
                          const newTerms = [...glossaryTerms];
                          newTerms[index].translation = e.target.value;
                          setGlossaryTerms(newTerms);
                        }}
                      />
                    </div>
                    <button
                      onClick={() => removeGlossaryTerm(index)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
