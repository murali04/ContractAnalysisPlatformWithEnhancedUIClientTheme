import React, { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// 1️⃣ Define context
interface AuthContextType {
  username: string | null;
  login: (user: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// 2️⃣ Provider component
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [username, setUsername] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  // Load username from localStorage on mount
  useEffect(() => {
    const storedUser = localStorage.getItem("username");
    if (storedUser) {
      setLoading(false);
      setUsername(storedUser);
      navigate("/");
    } else {
      setLoading(false);
      navigate("/login");
    }
  }, []);

  // Login function
  const login = (user: string) => {
    localStorage.setItem("username", user);
    setLoading(false);
    setUsername(user);
    navigate("/");
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem("username");
    setUsername(null);
    navigate("/login");
  };

  return (
    <AuthContext.Provider value={{ username, login, logout }}>
      {loading ? (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center z-9999 text-white px-6">
          {/* Simple Purple Spinner */}
          <div className="border-white h-12 w-12 animate-spin rounded-full border-4 border-t-purple-500 mb-4"></div>

          {/* Text */}
          <p className="text-lg font-medium tracking-wide">Loading...</p>
        </div>
      ) : (
        children
      )}
    </AuthContext.Provider>
  );
};

// 3️⃣ Hook for easier usage
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
