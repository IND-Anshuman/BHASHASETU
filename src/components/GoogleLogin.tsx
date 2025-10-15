import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { LogOut, User, Loader2 } from 'lucide-react';

const GoogleLogin: React.FC = () => {
  // Get authentication state and functions from context
  const { user, signInWithGoogle, signOut, loading } = useAuth();

  // Show loading spinner while authentication is in progress
  if (loading) {
    return (
      <div className="flex items-center justify-center p-2">
        <Loader2 className="w-5 h-5 animate-spin text-emerald-600" />
        <span className="ml-2 text-sm text-slate-600">Loading...</span>
      </div>
    );
  }

  // If user is logged in, show user info and logout button
  if (user) {
    return (
      <div className="flex items-center space-x-3">
        {/* User profile section */}
        <div className="flex items-center space-x-2">
          {/* User avatar */}
          <div className="w-8 h-8 bg-gradient-to-r from-emerald-600 to-teal-600 rounded-full flex items-center justify-center">
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
          {/* User info */}
          <div className="text-sm">
            <p className="font-medium text-slate-800">
              {user.user_metadata?.full_name || user.email?.split('@')[0]}
            </p>
            <p className="text-xs text-slate-600">
              {user.user_metadata?.provider === 'google' ? 'Google Account' : 'User'}
            </p>
          </div>
        </div>
        {/* Logout button */}
        <button
          onClick={signOut}
          className="flex items-center space-x-1 px-3 py-1.5 text-sm text-slate-600 hover:text-red-600 transition-colors rounded-lg hover:bg-red-50"
        >
          <LogOut className="w-4 h-4" />
          <span>Logout</span>
        </button>
      </div>
    );
  }

  // If user is not logged in, show Google sign-in button
  return (
    <button
      onClick={signInWithGoogle}
      className="flex items-center space-x-3 px-4 py-2 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-all shadow-sm hover:shadow-md"
    >
      {/* Google logo SVG */}
      <svg className="w-5 h-5" viewBox="0 0 24 24">
        <path
          fill="#4285F4"
          d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
        />
        <path
          fill="#34A853"
          d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
        />
        <path
          fill="#FBBC05"
          d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
        />
        <path
          fill="#EA4335"
          d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
        />
      </svg>
      <span className="text-slate-700 font-medium">Sign in with Google</span>
    </button>
  );
};

export default GoogleLogin;


