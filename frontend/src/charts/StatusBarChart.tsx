import {
  Bar,
  BarChart,
  Cell,
  LabelList,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useChartVisible } from "../hooks/useChartVisible";

interface StatusItem {
  name: string;
  value: number;
  fill: string;
}

interface StatusBarChartProps {
  data: StatusItem[];
}

const StatusBarChart: React.FC<StatusBarChartProps> = ({ data }) => {
  const { ref, visible } = useChartVisible(0.4);

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (!active || !payload?.length) return null;

    return (
      <div className="backdrop-blur-md bg-white/90 text-gray-800 px-3 py-2 rounded-xl shadow-lg border border-white/40">
        <div className="flex items-center">
          <p className="text-lg font-semibold">{payload[0].value}</p>
          <p className="text-sm font-medium ml-2">{label} obligations</p>
        </div>
      </div>
    );
  };

  return (
    <div className="h-full relative" ref={ref}>
      <ResponsiveContainer>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 15, right: 10, left: 10, bottom: 80 }}
        >
          <XAxis type="number" hide />
          <YAxis
            type="category"
            dataKey="name"
            tickLine={false}
            tick={false}
            mirror
          />

          <Tooltip cursor={{ fill: "#f1f5f9" }} content={<CustomTooltip />} />

          <Bar
            dataKey="value"
            barSize={15}
            radius={[0, 10, 10, 0]}
            isAnimationActive={visible} // enable animation
            animationDuration={5000}
          >
            {data.map((item, index) => (
              <Cell key={index} fill={item.fill} />
            ))}
            <LabelList position="center" fill="#fff" fontSize={12} />
          </Bar>

          <Legend
            verticalAlign="bottom"
            height={6}
            payload={data.map((d) => ({
              color: d.fill,
              type: "circle",
              value: d.name,
            }))}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export { StatusBarChart };
