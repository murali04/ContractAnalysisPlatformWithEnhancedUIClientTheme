import { useEffect, useState } from "react";

export function ScoreBar({ percentage }: any) {
  const [width, setWidth] = useState("0%");

  useEffect(() => {
    setTimeout(() => {
      setWidth(percentage);
    }, 100); // small delay to trigger animation
  }, [percentage]);

  return (
    <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
      <div
        className="h-2 rounded-full transition-all duration-3000 ease-out"
        style={{
          width: width,
          backgroundColor: "#A100FF",
        }}
      />
    </div>
  );
}
