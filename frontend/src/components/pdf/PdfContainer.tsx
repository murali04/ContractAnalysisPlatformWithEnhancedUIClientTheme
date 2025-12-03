import { ExternalLink, FileText } from "lucide-react";
import { useEffect, useState } from "react";
import { PdfViewer } from "./PdfViewer";

export function PdfContainer({
  analysisData,
  file,
  selectedClause,
  defaultScale,
}: any) {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  useEffect(() => {
    if (file) {
      const url = URL.createObjectURL(file);
      setPdfUrl(url);
      return () => URL.revokeObjectURL(url);
    }
  }, [file]);

  return (
    <div className="bg-white/90 backdrop-blur-sm border border-purple-200 rounded-xl p-3 h-[600px] flex flex-col shadow-lg">
      <div className="flex justify-between items-center mb-4 pb-3 border-b border-purple-200">
        <span className="text-xl flex items-center gap-2">
          <FileText className="w-5 h-5 text-purple-600" />
          <span className="text-gray-900 text-lg font-medium">
            Contract Preview
          </span>
        </span>
        <a
          href={analysisData?.contract_url}
          target="_blank"
          className="text-md text-blue-600 hover:text-blue-800 flex items-center gap-1 font-medium cursor-pointer"
        >
          Open Original <ExternalLink size={12} />
        </a>
      </div>
      <div className="flex-1 bg-white rounded border border-purple-300 overflow-hidden relative shadow-inner">
        {pdfUrl ? (
          <PdfViewer
            url={pdfUrl}
            selectedClause={selectedClause}
            defaultScale={defaultScale}
          />
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-900">
              {analysisData?.full_text || "No pdf loaded."}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
