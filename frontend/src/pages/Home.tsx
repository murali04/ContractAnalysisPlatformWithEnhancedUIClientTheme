import axios from "axios";
import { useState } from "react";
import { AnalysisResults } from "../components/AnalysisResults";
import { FileUpload } from "../components/FileUpload";
import { ProgressBar } from "../components/reusable/ProgressBar";

export const Home = () => {
  const [excelFile, setExcelFile] = useState<File | null>(null);
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [analysisData, setAnalysisData] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!excelFile || !pdfFile) {
      alert("Please upload both Excel and PDF files");
      return;
    }

    setIsAnalyzing(true);
    setProgress(0);
    setShowResults(false);

    // Start simulated progress
    const interval = setInterval(() => {
      setProgress((p) => (p < 90 ? p + 5 : p)); // stop at 90%
    }, 300);

    try {
      const formData = new FormData();
      formData.append("obligations_file", excelFile);
      formData.append("contract_file", pdfFile);
      formData.append("use_batch", "true");

      const res = await axios.post("http://localhost:8000/api/analyze/enhanced", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log(res.data);
      setAnalysisData(res.data);

      clearInterval(interval);
      setProgress(100);
      setIsAnalyzing(false);
      setShowResults(true);
    } catch (err) {
      console.log(err);
      clearInterval(interval);
      setIsAnalyzing(false);
      alert("Analysis failed. Please try again.");
    }
  };

  const handleReset = () => {
    setExcelFile(null);
    setPdfFile(null);
    setIsAnalyzing(false);
    setProgress(0);
    setShowResults(false);
    setAnalysisData(null);
  };
  return (
    <div>
      {/* Progress Bar */}
      {isAnalyzing && <ProgressBar progress={progress} />}

      {/* Upload Section */}
      <div className="">
        <FileUpload
          excelFile={excelFile}
          pdfFile={pdfFile}
          onExcelUpload={setExcelFile}
          onPdfUpload={setPdfFile}
          onAnalyze={handleAnalyze}
          onReset={handleReset}
          isAnalyzing={isAnalyzing}
          showResults={showResults}
        />
      </div>

      {/* Analysis Results */}
      {!isAnalyzing && showResults && analysisData && (
        <div className="mt-8">
          <AnalysisResults pdfFile={pdfFile} analysisData={analysisData} />
        </div>
      )}
    </div>
  );
};
