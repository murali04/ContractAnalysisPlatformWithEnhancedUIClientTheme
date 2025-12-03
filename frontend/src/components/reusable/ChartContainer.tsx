interface ChartContainerProps {
  title: string;
  children: React.ReactNode;
}

const ChartContainer: React.FC<ChartContainerProps> = ({ title, children }) => {
  return (
    <div className='bg-linear-to-br from-backdrop-linear-primary to-backdrop-linear-secondary border border-purple-200 rounded-xl p-4 h-56 shadow-md hover:shadow-xl transition-shadow'>
      <span className='text-lg text-title-primary'>{title}</span>
      <div className='w-full h-full mt-3 hover:scale-105 hover:bg-white/40 transition-all duration-300 relative'>
        {children}
      </div>
    </div>
  );
};

export default ChartContainer;
