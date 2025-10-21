import { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LandingPage from './pages/LandingPage';
import LearnerModule from './pages/LearnerModule';
import AdminDashboard from './pages/AdminDashboard';
import TranslationModule from './pages/TranslationModule';
import VoiceModule from './pages/VoiceModule';
import AuthCallback from './pages/AuthCallback';

type Page = 'landing' | 'learner' | 'admin' | 'translation' | 'voice';

// Inner component that has access to authentication context
function AppContent() {
  const [currentPage, setCurrentPage] = useState<Page>('landing');
  const { user } = useAuth();

  // Handle auth callback route
  if (window.location.pathname === '/auth/callback') {
    return <AuthCallback />;
  }

  // If user is authenticated and on landing page, redirect to learner module
  if (user && currentPage === 'landing') {
    // Use setTimeout to avoid state update during render
    setTimeout(() => setCurrentPage('learner'), 0);
  }

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

// Main App component wrapped with AuthProvider
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
