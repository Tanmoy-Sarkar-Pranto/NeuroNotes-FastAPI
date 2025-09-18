import React, { createContext, useContext, useEffect, useState } from 'react';
import { apiService } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      const token = apiService.getAuthToken();
      if (token) {
        try {
          const userData = await apiService.getCurrentUser();
          setUser(userData);
        } catch (error) {
          console.error('Failed to get user data:', error);

          // Only remove token if it's a clear authentication error
          if (error.message.includes('credentials') ||
              error.message.includes('Unauthorized') ||
              error.message.includes('Invalid token')) {
            console.log('Removing invalid token due to auth error');
            apiService.removeAuthToken();
            setUser(null);
          } else {
            // For other errors (network, server errors), try to preserve auth state
            // We'll create a minimal user object from the token if possible
            console.warn('Network or server error during user fetch, preserving auth state');

            // Try to decode basic info from token or use a placeholder
            setUser({
              id: 'temp',
              username: 'User',
              email: 'user@example.com'
            });
          }
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (credentials) => {
    try {
      const response = await apiService.login(credentials);
      apiService.setAuthToken(response.access_token);

      // For login, we already have the user data in the response
      setUser({
        id: response.id,
        username: response.username,
        email: response.email,
      });
    } catch (error) {
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      const response = await apiService.register(userData);
      // Registration doesn't return a token, so we need to login after registration
      await login({ email: userData.email, password: userData.password });
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    apiService.removeAuthToken();
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};