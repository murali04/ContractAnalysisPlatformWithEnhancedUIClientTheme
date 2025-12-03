import { useState } from "react";
import { StatusBadge } from "./StatusBadge";
import SearchBox from "./reusable/SearchBox";

export const ItemsList = ({
  analysisData,
  selectedObligation,
  handleChangeObligation,
}: any) => {
  const [searchText, setSearchText] = useState("");
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchText(e.target.value);
  };

  const filterAnalysisData = analysisData.results.filter((res: any) =>
    res?.obligation?.toLowerCase().includes(searchText?.toLowerCase() || "")
  );

  return (
    <div className="bg-white/90 backdrop-blur-sm border border-purple-200 rounded-xl p-3 h-[600px] flex flex-col shadow-lg">
      <div className="mb-4 pb-3 border-b border-purple-200">
        <span className="text-gray-900 text-lg font-medium">Obligations</span>
        {/* <div className="flex items-center gap-2 text-sm mt-3">
          <span className="inline-flex items-center gap-2 px-1.5 py-1.5 bg-green-50 text-green-700 rounded-lg border border-green-200 shadow-sm">
            <Check className="w-6 h-6" />3 Compliance
          </span>

          <span className="inline-flex items-center gap-2 px-1.5 py-1.5 bg-red-50 text-red-700 rounded-lg border border-red-200 shadow-sm">
            <X className="w-6 h-6" />3 Non Compliance
          </span>
        </div> */}
      </div>

      {/* Filter/Search Section */}
      <div className="mb-3">
        <SearchBox searchText={searchText} setSearchText={setSearchText} />
      </div>

      <div
        className="flex-1 overflow-y-auto space-y-3"
        style={{
          scrollbarWidth: "thin",
          scrollbarColor: "#A100FF #f0f0f0",
        }}
      >
        {filterAnalysisData?.length > 0 ? (
          filterAnalysisData.map((res: any, idx: number) => {
            return (
              <button
                key={idx}
                onClick={() => handleChangeObligation(res)}
                className={`p-4 border-b border-slate-100 cursor-pointer text-left transition-colors rounded-md ${selectedObligation === res
                  ? "bg-indigo-50 border-l-4 border-l-indigo-600"
                  : "hover:bg-slate-50 border-l-4 border-l-transparent"
                  }`}
              >
                <div className="flex justify-between items-start mb-2">
                  <StatusBadge status={res.is_present} />

                </div>
                <p
                  className={`text-sm font-medium ${selectedObligation === res
                    ? "text-indigo-900"
                    : "text-slate-600"
                    }`}
                >
                  {res.obligation}
                </p>
              </button>
            );
          })
        ) : (
          <span className="p-4 text-sm font-medium text-slate-600">
            No obligations
          </span>
        )}
      </div>
    </div>
  );
};
