import { useEffect } from 'react';
import { supabase } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';

const AuthCallback: React.FC = () => {
  const { user } = useAuth();

  useEffect(() => {
    // Handle the OAuth callback from Google
    const handleAuthCallback = async () => {
      try {
        // Wait a bit for the auth context to update
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        if (user) {
          console.log('Authentication successful:', user.email);
          // Redirect to learner module after successful authentication
          window.location.href = '/';
        } else {
          // Check if there's a session in the URL
          const { data, error } = await supabase.auth.getSession();
          
          if (error) {
            console.error('Error handling auth callback:', error);
            window.location.href = '/?error=auth_failed';
            return;
          }
          
          if (data.session) {
            console.log('Authentication successful:', data.session.user.email);
            window.location.href = '/';
          } else {
            // No session found, redirect to home
            window.location.href = '/';
          }
        }
      } catch (error) {
        console.error('Unexpected error during auth callback:', error);
        window.location.href = '/?error=unexpected_error';
      }
    };

    // Call the handler when component mounts
    handleAuthCallback();
  }, [user]);

  // Loading screen while processing authentication
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-emerald-50/30 to-teal-50/40 flex items-center justify-center">
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-slate-200/50 p-8 text-center max-w-md mx-4">
        {/* Loading spinner */}
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-emerald-600 mx-auto mb-6"></div>
        
        {/* Loading message */}
        <h2 className="text-2xl font-semibold text-slate-800 mb-3">
          Completing Sign In
        </h2>
        <p className="text-slate-600 mb-4">
          Please wait while we complete your authentication with Google...
        </p>
        
        {/* Progress indicator */}
        <div className="w-full bg-slate-200 rounded-full h-2">
          <div className="bg-gradient-to-r from-emerald-600 to-teal-600 h-2 rounded-full animate-pulse" style={{width: '70%'}}></div>
        </div>
        
        <p className="text-sm text-slate-500 mt-4">
          This will only take a moment
        </p>
      </div>
    </div>
  );
};

export default AuthCallback;


