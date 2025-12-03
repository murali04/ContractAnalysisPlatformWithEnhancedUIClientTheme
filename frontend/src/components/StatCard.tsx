interface StatCardProps {
  label: string;
  value: string | number;
  fromColor: string;
  toColor: string;
  labelColor: string;
  icon: React.ReactNode;
}

const StatCard: React.FC<StatCardProps> = ({
  label,
  value,
  fromColor,
  toColor,
  labelColor,
  icon,
}) => {
  return (
    <div
      className={`bg-linear-to-br ${fromColor} ${toColor} rounded-xl p-3 text-white shadow-lg hover:shadow-xl transition-shadow h-[108px]`}
    >
      <div className="flex items-center justify-between mb-2">
        <span className={`${labelColor} text-md mr-1`}>{label}</span>
        <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
          <span className="text-2xl">{icon}</span>
        </div>
      </div>
      <p className="text-xl font-medium">{value}</p>
    </div>
  );
};

export default StatCard;
