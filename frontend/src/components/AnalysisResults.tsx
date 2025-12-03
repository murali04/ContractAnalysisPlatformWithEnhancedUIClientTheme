import { useState } from "react";
import { RadialHealthChart } from "../charts/RadialHealthChart";
import { StatusBarChart } from "../charts/StatusBarChart";
import { useAuth } from "../context/AuthContext";
import { ItemsList } from "./ItemsList";
import { PdfContainer } from "./pdf/PdfContainer";
import ChartContainer from "./reusable/ChartContainer";
import StatCard from "./StatCard";
import { TabsPanel } from "./TabsPanel";

interface AnalysisResultsProps {
  pdfFile: File | null;
  analysisData: any;
}

export function AnalysisResults({
  pdfFile,
  analysisData,
}: AnalysisResultsProps) {
  // Get username from context or fallback to localStorage directly to ensure it displays
  const { username = "User" } = useAuth();

  const [selectedObligation, setSelectedObligation] = useState<
    null | (typeof analysisData.results)[0]
  >(null);
  const [selectedClause, setSelectedClause] = useState("");

  const handleChangeObligation = (obligation: any) => {
    setSelectedObligation(obligation);
    setSelectedClause(obligation.supporting_clauses.join("\n"));
  };

  const [openItemId, setOpenItemId] = useState<number | null>(null);
  const [selectedTab, setSelectedTab] = useState("details");
  // const [selectedClause, setSelectedClause] = useState(null);

  const toggleItem = (id: any) => {
    setOpenItemId((openItemId) => (openItemId === id ? null : id));
    setSelectedTab("details"); // reset tab when switching items
  };

  const handleChangeTab = (tab: string) => {
    setSelectedTab(tab);
    setSelectedClause("");
  };

  const getScoreContent = (score: number) => {
    if (score > 75) return { color: "text-red-600", text: "Bad" };
    if (score > 50) return { color: "text-red-600", text: "Average" };
    return { color: "text-green-600", text: "Good" };
  };

  // Calculate stats
  const results = analysisData?.results || [];
  const totalObligations = results.length;
  const compliantCount = results.filter(
    (r: any) => r.is_present === "Yes"
  ).length;
  const nonCompliantCount = results.filter(
    (r: any) => r.is_present === "No"
  ).length;

  // Calculate average confidence/score for radial chart
  // Ensure we handle potential string values or missing fields robustly
  // const avgScore = totalObligations > 0
  //   ? Math.round(
  //     results.reduce((acc: number, r: any) => {
  //       const val = parseFloat(r.confidence);
  //       return acc + (isNaN(val) ? 0 : val);
  //     }, 0) / totalObligations
  //   )
  //   : 0;

  const avgScore = Math.round((compliantCount / totalObligations) * 100) || 0;

  const radialData = [{ name: "Score", value: avgScore, fill: "#00a63e" }];

  const statusData = [
    { name: "Compliance", value: compliantCount, fill: "#00a63e" },
    { name: "Non Compliance", value: nonCompliantCount, fill: "#e7000b" },
  ];

  const changeClause = (clause: string) => {
    setSelectedClause(clause);
  };

  const [searchText, setSearchText] = useState("");

  const filterAnalysisResultsData = results.filter((res: any) =>
    res?.obligation?.toLowerCase().includes(searchText?.toLowerCase() || "")
  );

  const handleExportReport = () => {
    // Create CSV header
    const headers = [
      'Obligation',
      'Status',
      'Reason',
      'Confidence (%)',
      'Similarity Score',
      'Page',
      'Line',
      'Suggestion',
      'Supporting Clauses',
      'Validation Steps'
    ];

    // Create CSV rows
    const rows = results.map((r: any) => {
      const validationSteps = r.cot_steps?.map((step: any) =>
        `${step.step_name}: ${step.status} - ${step.finding}`
      ).join(' | ') || '';

      const supportingClauses = r.supporting_clauses?.join(' | ') || '';

      return [
        `"${(r.obligation || '').replace(/"/g, '""')}"`,
        r.is_present || '',
        `"${(r.reason || '').replace(/"/g, '""')}"`,
        r.confidence || '',
        r.similarity_score || '',
        r.page || '',
        r.line || '',
        `"${(r.suggestion || '').replace(/"/g, '""')}"`,
        `"${supportingClauses.replace(/"/g, '""')}"`,
        `"${validationSteps.replace(/"/g, '""')}"`
      ].join(',');
    });

    // Add summary section at the top
    const summaryRows = [
      ['Contract Analysis Report'],
      ['Export Date', new Date().toISOString()],
      ['Analyzed By', username || 'User'],
      ['Total Obligations', totalObligations],
      ['Compliant', compliantCount],
      ['Non-Compliant', nonCompliantCount],
      ['Compliance Score', `${avgScore}%`],
      [],
      headers
    ];

    const csvContent = [
      ...summaryRows.map(row => row.join(',')),
      ...rows
    ].join('\n');

    // Create and download the CSV file
    const BOM = '\uFEFF'; // UTF-8 BOM for Excel compatibility
    const dataBlob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `contract-analysis-report-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <div className="pt-4 bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-purple-100 p-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <span className="bg-linear-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent text-2xl font-bold block">
              Analysis Results
            </span>
            <span className="text-sm text-gray-500 font-medium">
              Welcome back, {username || "User"}
            </span>
          </div>
          <div className="flex gap-2">
            <button
              className="px-4 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-colors text-sm cursor-pointer"
              onClick={handleExportReport}
            >
              Export Report
            </button>
            <button
              className="px-4 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-colors text-sm cursor-pointer"
              onClick={() => print()}
            >
              Print
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6  mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div className="flex flex-col gap-2">
              <StatCard
                label="Total Obligations"
                value={totalObligations}
                fromColor="from-purple-500"
                toColor="to-purple-600"
                labelColor="text-purple-100"
                icon="📊"
              />
              <StatCard
                label="Compliance"
                value={compliantCount}
                fromColor="from-green-500"
                toColor="to-green-600"
                labelColor="text-green-100"
                icon="✓"
              />
            </div>
            <div className="flex flex-col gap-2">
              <StatCard
                label="Non Compliance"
                value={nonCompliantCount}
                fromColor="from-rose-400"
                toColor="to-rose-500"
                labelColor="text-red-100"
                icon="⚠"
              />
              <StatCard
                label="Processing Time"
                value="3.2s"
                fromColor="from-blue-500"
                toColor="to-blue-600"
                labelColor="text-blue-100"
                icon="⚡"
              />
            </div>
          </div>
          {/* Charts Section */}
          <ChartContainer title="Overall Health">
            <RadialHealthChart value={avgScore} radialData={radialData} />
          </ChartContainer>

          <ChartContainer title="Compliance Status Distribution">
            <StatusBarChart data={statusData} />
          </ChartContainer>
        </div>

        {/* Three Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left: Items List */}
          <div className="lg:col-span-3">
            <ItemsList
              handleChangeObligation={handleChangeObligation}
              analysisData={analysisData}
              selectedObligation={selectedObligation}
            />
          </div>

          {/* Center: PDF Viewer */}
          <div
            className={`lg:col-span-5 pdf-highlight-${selectedObligation?.is_present === "Yes"
              ? "compliance"
              : "non-compliance"
              }`}
          >
            <PdfContainer file={pdfFile} selectedClause={selectedClause} />
          </div>

          {/* Right: Tabs Panel */}
          <div className="lg:col-span-4">
            <TabsPanel
              selectedObligation={selectedObligation}
              selectedClause={selectedClause}
              setSelectedClause={setSelectedClause}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
