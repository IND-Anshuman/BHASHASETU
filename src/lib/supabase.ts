import { createClient } from '@supabase/supabase-js';

// Supabase configuration
// You'll replace these with your actual Supabase project credentials
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://ysuummbmblioexpnxlrf.supabase.co';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlzdXVtbWJtYmxpb2V4cG54bHJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTQ5NTIsImV4cCI6MjA3NjAzMDk1Mn0.Sh81VhjLtYr2ouq0zQKK46GvTlbQOIZHpW29CnQxDKQ';

// Create Supabase client with authentication settings
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,    // Automatically refresh tokens when they expire
    persistSession: true,      // Keep user logged in between browser sessions
    detectSessionInUrl: true   // Detect authentication callback in URL
  }
});

// Export TypeScript types for better development experience
export type { User, Session, AuthError } from '@supabase/supabase-js';







