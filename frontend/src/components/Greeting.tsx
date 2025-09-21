import React, { useState, useEffect } from 'react';
import { useTheme } from '../contexts/ThemeContext';

interface GreetingResponse {
  message: string;
  status: string;
}

export default function Greeting() {
  const { theme } = useTheme();
  const [greeting, setGreeting] = useState<GreetingResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchGreeting = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/hello');
      if (!response.ok) {
        throw new Error('Failed to fetch greeting');
      }
      const data = await response.json();
      setGreeting(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGreeting();
  }, []);

  return (
    <div className={`backdrop-blur-md border rounded-xl p-6 transition-colors duration-300 ${ 
      theme === 'light' 
        ? 'bg-white/80 border-slate-200 shadow-lg' 
        : 'bg-white/5 border-white/10'
    }`}>
      <div className="flex items-center gap-3 mb-4">
        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center">
          <span className="text-white font-semibold">👋</span>
        </div>
        <h3 className={`text-lg font-semibold transition-colors duration-300 ${ 
          theme === 'light' ? 'text-slate-800' : 'text-white'
        }`}>
          Welcome Message
        </h3>
      </div>
      
      {loading && (
        <div className={`animate-pulse transition-colors duration-300 ${ 
          theme === 'light' ? 'text-slate-600' : 'text-white/70'
        }`}>
          Loading greeting...
        </div>
      )}
      
      {error && (
        <div className={`text-red-500 transition-colors duration-300 ${ 
          theme === 'light' ? 'bg-red-50 border-red-200' : 'bg-red-900/20 border-red-800'
        } border rounded-lg p-3`}>
          {error}
        </div>
      )}
      
      {greeting && (
        <div className="space-y-3">
          <div className={`transition-colors duration-300 ${ 
            theme === 'light' ? 'text-slate-700' : 'text-white/90'
          }`}>
            {greeting.message}
          </div>
          <div className="flex items-center gap-2">
            <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${ 
              greeting.status === 'ready' 
                ? theme === 'light' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-green-900/30 text-green-400'
                : theme === 'light' 
                  ? 'bg-gray-100 text-gray-800' 
                  : 'bg-gray-900/30 text-gray-400'
            }`}>
              <div className={`h-1.5 w-1.5 rounded-full mr-1.5 ${ 
                greeting.status === 'ready' ? 'bg-green-500' : 'bg-gray-500'
              }`}></div>
              {greeting.status === 'ready' ? 'System Ready' : greeting.status}
            </div>
            <button 
              onClick={fetchGreeting}
              className={`text-xs px-3 py-1 rounded-lg font-medium transition-all duration-200 hover:scale-105 ${ 
                theme === 'light' 
                  ? 'bg-blue-100 text-blue-700 hover:bg-blue-200' 
                  : 'bg-blue-900/30 text-blue-300 hover:bg-blue-900/50'
              }`}
            >
              Refresh
            </button>
          </div>
        </div>
      )}
    </div>
  );
}