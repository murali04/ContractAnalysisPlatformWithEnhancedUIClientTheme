import { CircleX } from "lucide-react";

export default function SearchBox({ searchText, setSearchText }: any) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchText(e.target.value);
  };
  return (
    <div className="relative w-full">
      {/* Search Icon */}
      <svg
        className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 104.5 4.5a7.5 7.5 0 0012.15 12.15z"
        />
      </svg>

      {/* Input Field */}
      <input
        type="text"
        placeholder="Search..."
        value={searchText}
        onChange={handleChange}
        className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none"
      />

      {/* Clear Icon (shows only when typing) */}
      {searchText && (
        <button
          onClick={() => setSearchText("")}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-purple-600 cursor-pointer"
        >
          <CircleX />
        </button>
      )}
    </div>
  );
}
