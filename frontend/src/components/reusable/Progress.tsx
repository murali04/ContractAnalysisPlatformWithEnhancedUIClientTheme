export const Progress = ({ progress }: any) => {
  return (
    <div className="w-[50%] bg-gray-200 rounded-full h-3 overflow-hidden shadow-inner">
      <div
        className="h-full transition-all duration-300 ease-out rounded-full"
        style={{ width: `${progress}%`, backgroundColor: "#A100FF" }}
      ></div>
    </div>
  );
};
