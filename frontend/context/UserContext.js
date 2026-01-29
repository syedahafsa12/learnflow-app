import React, { createContext, useState, useContext, useEffect } from 'react';

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState({ name: 'Student Maya', role: 'student' });

  const toggleRole = () => {
    setUser(prev => ({
      ...prev,
      role: prev.role === 'student' ? 'teacher' : 'student',
      name: prev.role === 'student' ? 'Professor Rodriguez' : 'Student Maya'
    }));
  };

  return (
    <UserContext.Provider value={{ user, toggleRole }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};
