import {
  ChartNetwork,
  HelpCircle,
  LogOut,
  Settings,
  User,
  UserCircle,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "../../context/AuthContext";

export function Header() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const { username, logout } = useAuth();

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <header className="bg-white/80 backdrop-blur-lg border-b border-purple-100 shadow-sm relative z-10">
      <div className="max-w-7xl mx-auto px-6 py-2">
        <div className="flex items-center justify-between">
          <span className="flex gap-2 items-center">
            <ChartNetwork height={40} width={40} className="text-purple-600" />
            <span className="text-2xl mb-1 bg-linear-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Contract Intel
            </span>
          </span>

          {/* Profile Dropdown */}

          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="flex items-center gap-2 p-2 rounded-full hover:bg-purple-50 transition-all hover:shadow-md align-center cursor-pointer"
            >
              {username}
              <div
                className="w-10 h-10 rounded-full flex items-center justify-center text-white shadow-lg hover:shadow-xl transition-shadow"
                style={{
                  background:
                    "linear-gradient(135deg, #A100FF 0%, #FF00E5 100%)",
                }}
              >
                <User className="w-6 h-6" />
              </div>
            </button>

            {/* Dropdown Menu */}
            {isDropdownOpen && (
              <div className="absolute right-0 mt-3 w-64 bg-white rounded-xl shadow-2xl border border-purple-100 py-2 animate-in fade-in slide-in-from-top-2 duration-200">
                <div className="px-4 py-3 border-b border-purple-100 bg-linear-to-r from-purple-50 to-pink-50">
                  <p className="text-gray-900">{username}</p>
                  <p className="text-sm text-gray-500">{username}@example.com</p>
                </div>

                <button
                  className="w-full px-4 py-2.5 text-left text-gray-700 hover:bg-purple-50 flex items-center gap-3 transition-colors rounded-lg mx-1 cursor-pointer"
                  onClick={() => setIsDropdownOpen(false)}
                >
                  <UserCircle className="w-5 h-5 text-purple-500" />
                  <span>Profile</span>
                </button>

                <button
                  className="w-full px-4 py-2.5 text-left text-gray-700 hover:bg-purple-50 flex items-center gap-3 transition-colors rounded-lg mx-1 cursor-pointer"
                  onClick={() => setIsDropdownOpen(false)}
                >
                  <Settings className="w-5 h-5 text-purple-500" />
                  <span>Settings</span>
                </button>

                <button
                  className="w-full px-4 py-2.5 text-left text-gray-700 hover:bg-purple-50 flex items-center gap-3 transition-colors rounded-lg mx-1 cursor-pointer"
                  onClick={() => setIsDropdownOpen(false)}
                >
                  <HelpCircle className="w-5 h-5 text-purple-500" />
                  <span>Help</span>
                </button>

                <div className="border-t border-purple-100 mt-2 pt-2">
                  <button
                    className="w-full px-4 py-2.5 text-left text-red-600 hover:bg-red-50 flex items-center gap-3 transition-colors rounded-lg mx-1 cursor-pointer"
                    onClick={() => {
                      setIsDropdownOpen(false);
                      logout();
                    }}
                  >
                    <LogOut className="w-5 h-5" />
                    <span>Logout</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
