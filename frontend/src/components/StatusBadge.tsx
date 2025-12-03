export const StatusBadge = ({ status }: { status: string }) => {
  const config: Record<string, { bg: string; text: string; border: string; label: string }> = {
    Yes: {
      bg: "bg-emerald-50",
      text: "text-emerald-700",
      border: "border-emerald-200",
      label: "Compliance",
    },
    No: {
      bg: "bg-rose-50",
      text: "text-rose-700",
      border: "border-rose-200",
      label: "Non-Compliance",
    },
  };
  const style = (status && config[status]) || {
    bg: "bg-slate-50",
    text: "text-slate-700",
    border: "border-slate-200",
    label: status,
  };

  return (
    <span
      className={`px-3 py-1 rounded-md text-[12px] font-bold border ${style.bg} ${style.text} ${style.border} tracking-wide`}
    >
      {style.label}
    </span>
  );
};
