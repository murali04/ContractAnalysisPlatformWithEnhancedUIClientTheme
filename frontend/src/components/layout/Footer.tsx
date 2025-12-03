export const Footer = () => {
  return (
    <footer className="fixed bottom-0 left-0 w-full bg-linear-to-r from-purple-600 to-pink-600 text-white py-4 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-3 md:gap-0">
        {/* Footer Text */}
        <p className="text-sm text-center md:text-left">
          © 2025 Contract Intel. All rights reserved.
        </p>

        {/* Links */}
        <div className="flex space-x-4 text-sm">
          <a href="#" className="hover:text-gray-200 transition">
            Privacy
          </a>
          <a href="#" className="hover:text-gray-200 transition">
            Terms
          </a>
          <a href="#" className="hover:text-gray-200 transition">
            Contact
          </a>
        </div>
      </div>
    </footer>
  );
};
