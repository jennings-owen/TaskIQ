import React, { useState } from 'react';
import { SignIn } from './SignIn';
import { Register } from './Register';

export const AuthPage = () => {
  const [isSignIn, setIsSignIn] = useState(true);

  const toggleMode = () => {
    setIsSignIn(!isSignIn);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">
            Agile TaskIQ
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            Your intelligent task management system
          </p>
        </div>
        
        {isSignIn ? (
          <SignIn onToggleMode={toggleMode} />
        ) : (
          <Register onToggleMode={toggleMode} />
        )}
      </div>
    </div>
  );
};