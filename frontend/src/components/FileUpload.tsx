import { FileSpreadsheet, FileText, Upload, X } from "lucide-react";
import { useRef } from "react";

interface FileUploadProps {
  excelFile: File | null;
  pdfFile: File | null;
  onExcelUpload: (file: File | null) => void;
  onPdfUpload: (file: File | null) => void;
  onAnalyze: () => void;
  onReset: () => void;
  isAnalyzing: boolean;
  showResults: boolean;
}

export function FileUpload({
  excelFile,
  pdfFile,
  onExcelUpload,
  onPdfUpload,
  onAnalyze,
  onReset,
  isAnalyzing,
  showResults,
}: FileUploadProps) {
  const excelRef = useRef<HTMLInputElement>(null);
  const pdfRef = useRef<HTMLInputElement>(null);
  const handleExcelChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onExcelUpload(file);
    }
  };

  const handlePdfChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onPdfUpload(file);
    }
  };

  const onFilesReset = () => {
    onReset();
    resetExcel();
    resetPdf();
  };

  const resetPdf = () => {
    if (pdfRef?.current) pdfRef.current.value = "";
  };

  const resetExcel = () => {
    if (excelRef?.current) excelRef.current.value = "";
  };

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-purple-100 p-5">
      <div className="flex flex-col justify-center relative overflow-hidden">
        <div className="relative">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/30 border border-indigo-400/30 mb-2">
            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
            <span className="text-xs font-semibold tracking-wide">
              v2.5 Enterprise
            </span>
          </div>
          <h1 className="text-5xl leading-16 mb-2 bg-linear-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            Contract Intelligence Platform
          </h1>
          <p className="text-lg mb-2">
            Automated compliance verification powered by advanced RAG
            technology.
            <br />
            Upload your documents to begin.
          </p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4 mt-6">
        {/* Excel Upload */}
        <div>
          <label className="block text-gray-700 mb-3">
            <span className="flex items-center gap-2">
              <FileSpreadsheet className="w-4 h-4 text-purple-500" />
              Upload Obligations File
            </span>
          </label>
          <div className="relative">
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleExcelChange}
              className="hidden"
              id="excel-upload"
              disabled={isAnalyzing}
              ref={excelRef}
            />
            <label
              htmlFor="excel-upload"
              className={`flex flex-col items-center justify-center gap-3 p-3 border-2 border-dashed rounded-xl cursor-pointer transition-all min-h-10 ${
                excelFile
                  ? "border-green-400 bg-linear-to-br from-green-50 to-emerald-50 shadow-md"
                  : "border-purple-200 hover:border-purple-400 bg-linear-to-br from-purple-50 to-pink-50 hover:shadow-lg"
              } ${isAnalyzing ? "opacity-50 cursor-not-allowed" : ""}`}
            >
              {excelFile ? (
                <div className="flex gap-6">
                  <div className="w-12 h-12 bg-green-200 rounded-full flex items-center justify-center">
                    <FileSpreadsheet className="w-6 h-6 text-green-600" />
                  </div>
                  <div className="text-center flex-1">
                    <p className="text-green-900 truncate max-w-[200px]">
                      {excelFile.name}
                    </p>
                    <p className="text-xs text-green-600 mt-1">
                      {(excelFile.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      onExcelUpload(null);
                      resetExcel();
                    }}
                    className="absolute top-2 right-2 p-1 bg-white rounded-full shadow-sm hover:shadow-md"
                    disabled={isAnalyzing}
                  >
                    <X className="w-4 h-4 text-gray-500 hover:text-gray-700 cursor-pointer" />
                  </button>
                </div>
              ) : (
                <div className="flex gap-6">
                  <div className="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center">
                    <Upload className="w-6 h-6 text-purple-600" />
                  </div>
                  <div className="text-center">
                    <p className="text-gray-700">Drop Excel file here</p>
                    <p className="text-xs text-gray-500 mt-1">
                      or click to browse
                    </p>
                  </div>
                </div>
              )}
            </label>
          </div>
        </div>

        {/* PDF Upload */}
        <div>
          <label className="block text-gray-700 mb-3">
            <span className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-purple-500" />
              Upload Contract File
            </span>
          </label>
          <div className="relative">
            <input
              type="file"
              accept=".pdf"
              onChange={handlePdfChange}
              className="hidden"
              id="pdf-upload"
              disabled={isAnalyzing}
              ref={pdfRef}
            />
            <label
              htmlFor="pdf-upload"
              className={`flex flex-col items-center justify-center gap-3 p-3 border-2 border-dashed rounded-xl cursor-pointer transition-all min-h-10 ${
                pdfFile
                  ? "border-green-400 bg-linear-to-br from-green-50 to-emerald-50 shadow-md"
                  : "border-purple-200 hover:border-purple-400 bg-linear-to-br from-purple-50 to-pink-50 hover:shadow-lg"
              } ${isAnalyzing ? "opacity-50 cursor-not-allowed" : ""}`}
            >
              {pdfFile ? (
                <div className="flex gap-6">
                  <div className="w-12 h-12 bg-green-200 rounded-full flex items-center justify-center">
                    <FileText className="w-6 h-6 text-green-600" />
                  </div>
                  <div className="text-center flex-1">
                    <p className="text-green-900 truncate max-w-[200px]">
                      {pdfFile.name}
                    </p>
                    <p className="text-xs text-green-600 mt-1">
                      {(pdfFile.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      onPdfUpload(null);
                      resetPdf();
                    }}
                    className="absolute top-2 right-2 p-1 bg-white rounded-full shadow-sm hover:shadow-md"
                    disabled={isAnalyzing}
                  >
                    <X className="w-4 h-4 text-gray-500 hover:text-gray-700 cursor-pointer" />
                  </button>
                </div>
              ) : (
                <div className="flex gap-6">
                  <div className="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center">
                    <Upload className="w-6 h-6 text-purple-600" />
                  </div>
                  <div className="text-center">
                    <p className="text-gray-700">Drop PDF file here</p>
                    <p className="text-xs text-gray-500 mt-1">
                      or click to browse
                    </p>
                  </div>
                </div>
              )}
            </label>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="text-right">
        <button
          onClick={onAnalyze}
          disabled={!excelFile || !pdfFile || isAnalyzing}
          className="cursor-pointer mb-2 px-8 py-3 text-white rounded-xl hover:opacity-90 hover:shadow-xl disabled:bg-gray-300 disabled:cursor-not-allowed transition-all shadow-lg transform hover:scale-105"
          style={{
            background:
              !excelFile || !pdfFile || isAnalyzing
                ? undefined
                : "linear-gradient(135deg, #A100FF 0%, #FF00E5 100%)",
          }}
        >
          {isAnalyzing ? "Analyzing..." : "Analyze Documents"}
        </button>
        {showResults && (
          <button
            onClick={onFilesReset}
            className="cursor-pointer ml-4 px-8 py-3 bg-linear-to-r from-gray-100 to-gray-200 text-gray-700 rounded-xl hover:from-gray-200 hover:to-gray-300 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
          >
            Reset
          </button>
        )}
      </div>
    </div>
  );
}
