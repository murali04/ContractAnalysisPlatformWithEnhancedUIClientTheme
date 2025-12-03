import { useCallback, useEffect } from "react";
// Import the main component
import { Viewer, Worker } from "@react-pdf-viewer/core";
import { highlightPlugin, Trigger } from "@react-pdf-viewer/highlight";
import { searchPlugin } from "@react-pdf-viewer/search";
import { toolbarPlugin } from "@react-pdf-viewer/toolbar";
import { Progress } from "../reusable/Progress";

// Import the styles
import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/search/lib/styles/index.css";
import "@react-pdf-viewer/toolbar/lib/styles/index.css";
import "./pdf.css";

export const PdfViewer = ({
  url,
  selectedClause,
  defaultScale = 0.75,
}: any) => {
  const highlightPluginInstance = highlightPlugin({
    trigger: Trigger.None,
  });

  const toolbarPluginInstance = toolbarPlugin();
  const { Toolbar } = toolbarPluginInstance;

  const searchPluginInstance = searchPlugin();
  const { highlight, clearHighlights } = searchPluginInstance;

  const splitByNewline = useCallback(
    (text: string) =>
      text
        .split(/\r?\n/) // splits on \n or \r\n
        .map((line) => line.trim()) // optional: remove leading/trailing spaces
        .filter((line) => line.length > 0), // remove empty lines
    []
  );

  useEffect(() => {
    clearHighlights();
    if (selectedClause) {
      const clauseList = splitByNewline(selectedClause);
      highlight(clauseList);
    }
  }, [selectedClause, splitByNewline]);

  if (!url) return null;
  return (
    <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
      <div
        style={{
          borderBottom: "1px solid #ccc",
          padding: "4px",
          background: "#f8f8f8",
        }}
      >
        <Toolbar />
      </div>
      <Viewer
        defaultScale={defaultScale}
        fileUrl={url}
        renderLoader={(percentages: number) => (
          <div style={{ width: "240px" }}>
            <Progress progress={Math.round(percentages)} />
          </div>
        )}
        plugins={[
          highlightPluginInstance,
          toolbarPluginInstance,
          searchPluginInstance,
        ]}
      />
    </Worker>
  );
};
