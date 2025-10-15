import React, { createContext, useContext, useEffect, useState } from 'react';
import { User, Session } from '@supabase/supabase-js';
import { supabase } from '../lib/supabase';

// Define the shape of our authentication context
interface AuthContextType {
  user: User | null;                    // Current logged-in user (null if not logged in)
  session: Session | null;              // Current session data
  loading: boolean;                     // Loading state for authentication
  signInWithGoogle: () => Promise<void>; // Function to sign in with Google
  signOut: () => Promise<void>;         // Function to sign out
}

// Create the context with undefined as default value
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Props for the AuthProvider component
interface AuthProviderProps {
  children: React.ReactNode;
}

// Main authentication provider component
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  // State variables to track authentication status
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  // Effect to handle authentication state changes
  useEffect(() => {
    // Get the current session when component mounts
    const getInitialSession = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      setSession(session);
      setUser(session?.user ?? null);
      setLoading(false);
    };

    getInitialSession();

    // Listen for authentication state changes (login, logout, token refresh)
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        console.log('Auth state changed:', event, session?.user?.email);
        setSession(session);
        setUser(session?.user ?? null);
        setLoading(false);
      }
    );

    // Cleanup subscription when component unmounts
    return () => subscription.unsubscribe();
  }, []);

  // Function to sign in with Google
  const signInWithGoogle = async () => {
    try {
      setLoading(true);
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback` // Where to redirect after login
        }
      });
      if (error) throw error;
    } catch (error) {
      console.error('Error signing in with Google:', error);
      alert('Failed to sign in with Google. Please try again.');
      setLoading(false);
    }
  };

  // Function to sign out
  const signOut = async () => {
    try {
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
    } catch (error) {
      console.error('Error signing out:', error);
      alert('Failed to sign out. Please try again.');
    }
    // After sign out, optionally redirect to home to reset app state
    try {
      window.location.href = '/';
    } catch (_) {
      // no-op for non-browser environments
    }
  };

  // Value object to provide to all child components
  const value = {
    user,
    session,
    loading,
    signInWithGoogle,
    signOut
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};


