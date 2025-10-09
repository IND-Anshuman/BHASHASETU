import { useState } from 'react';
import LandingPage from './pages/LandingPage';
import LearnerModule from './pages/LearnerModule';
import AdminDashboard from './pages/AdminDashboard';
import TranslationModule from './pages/TranslationModule';
import VoiceModule from './pages/VoiceModule';

type Page = 'landing' | 'learner' | 'admin' | 'translation' | 'voice';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('landing');

  const renderPage = () => {
    switch (currentPage) {
      case 'landing':
        return <LandingPage onNavigate={setCurrentPage} />;
      case 'learner':
        return <LearnerModule onNavigate={setCurrentPage} />;
      case 'admin':
        return <AdminDashboard onNavigate={setCurrentPage} />;
      case 'translation':
        return <TranslationModule onNavigate={setCurrentPage} />;
      case 'voice':
        return <VoiceModule onNavigate={setCurrentPage} />;
      default:
        return <LandingPage onNavigate={setCurrentPage} />;
    }
  };

  return <>{renderPage()}</>;
}

export default App;
