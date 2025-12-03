import { User } from "lucide-react";
import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export const Login = () => {
  const { login, username } = useAuth();

  const [name, setName] = useState("");

  const handleSubmit = (e: any) => {
    e.preventDefault();
    if (name.trim()) {
      login(name);
    }
  };

  return (
    <div className="min-h-screen flex justify-center bg-slate-50 fade-in bg-linear-to-r from-purple-600 to-pink-600">
      {/* Left Pane - Branding */}
      <div className="flex flex-col justify-center p-20 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
        <div className="relative">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/30 border border-indigo-400/30 mb-6">
            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
            <span className="text-md font-semibold tracking-wide">
              v2.5 Enterprise
            </span>
          </div>
          <h1 className="text-6xl font-bold mb-6 leading-tight">
            Contract Intelligence <br />
            Platform
          </h1>
          <p className="text-indigo-100 text-xl max-w-md leading-relaxed">
            Automated compliance verification powered by advanced RAG
            technology.
            <br />
            Sign in to access your workspace.
          </p>
        </div>
      </div>

      {/* Right Pane - Login Form */}
      <div className="flex items-center justify-center p-12">
        <div className="w-full max-w-md bg-white p-10 rounded-2xl shadow-xl border border-slate-100">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4 text-indigo-600">
              <User size={32} />
            </div>
            <h2 className="text-2xl font-bold text-slate-800">Welcome Back</h2>
            <p className="text-slate-500 mt-2">
              Please enter your name to continue.
            </p>
          </div>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Full Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all"
                placeholder="e.g. Sarah Smith"
                autoFocus
                required
              />
            </div>
            <button
              type="submit"
              className="w-full py-3.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-lg shadow-indigo-200 transition-all transform hover:scale-[1.02]"
            >
              Enter Workspace
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
