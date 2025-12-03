import {
  PolarAngleAxis,
  RadialBar,
  RadialBarChart,
  ResponsiveContainer,
} from "recharts";
import { useChartVisible } from "../hooks/useChartVisible";

interface RadialHealthChartProps {
  value: number; // score percentage
  radialData: any;
}

const RadialHealthChart: React.FC<RadialHealthChartProps> = ({
  value,
  radialData,
}) => {
  const { ref, visible } = useChartVisible(0.4);

  return (
    <div className="h-full relative" ref={ref}>
      {/* Center Text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-2xl font-semibold text-gray-800 mb-10">
          {value}%
        </span>
      </div>

      <div className="absolute inset-0 flex flex-col items-center justify-center mt-13">
        <span className="text-lg text-gray-700">Health Score</span>
      </div>

      <ResponsiveContainer>
        <RadialBarChart
          cx="50%"
          cy="50%"
          innerRadius="100%"
          barSize={20}
          data={radialData}
          startAngle={180}
          endAngle={0}
        >
          <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
          <RadialBar
            background
            dataKey="value"
            cornerRadius={5}
            isAnimationActive={visible}
            animationDuration={5000}
          />
        </RadialBarChart>
      </ResponsiveContainer>
    </div>
  );
};

export { RadialHealthChart };
