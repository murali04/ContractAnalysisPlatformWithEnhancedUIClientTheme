import React, { JSX } from "react";
import { Navigate } from "react-router-dom";
import { Footer } from "../components/layout/Footer";
import { Header } from "../components/layout/Header";
import { useAuth } from "../context/AuthContext";

interface ProtectedRouteProps {
  children: JSX.Element;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { username } = useAuth();

  if (!username) {
    // Redirect to login page if not logged in
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-purple-50 via-white to-pink-50 pb-[50px]">
      {/* Header */}
      <Header />
      {children}
      <Footer />
    </div>
  );
};
