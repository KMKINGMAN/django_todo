import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { validateToken } from '../services/api';

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const redirectToLogin = useCallback(() => {
    navigate('/login');
  }, [navigate]);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      
      if (!token) {
        setIsAuthenticated(false);
        setLoading(false);
        return;
      }

      try {
        const response = await validateToken();
        setIsAuthenticated(true);
        setUser({
          id: response.data.user_id,
          username: response.data.username
        });
        
        // Update localStorage with fresh data
        localStorage.setItem('username', response.data.username);
      } catch (error) {
        console.error('Token validation failed:', error);
        setIsAuthenticated(false);
        setUser(null);
        
        // Clear invalid token
        localStorage.removeItem('token');
        localStorage.removeItem('username');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []); // Only run once on mount

  return {
    isAuthenticated,
    user,
    loading,
    redirectToLogin
  };
};

export default useAuth;
