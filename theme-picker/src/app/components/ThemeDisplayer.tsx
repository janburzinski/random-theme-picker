export const ThemeDisplayer: React.FC = ({}) => {
  // just data to test this out
  const theme = {
    thumbnail: "https://github.com/Mofiqul/vscode.nvim/raw/main/demo.png",
    description: "test miau test miautest .",
    downloads: 3248765,
  };

  return (
    <div className="flex justify-center items-center py-12">
      <div className="flex flex-col items-center bg-gradient-to-b from-gray-900 via-gray-800 to-black p-6 rounded-2xl shadow-xl max-w-md w-full text-center border border-gray-700">
        <img
          src={theme.thumbnail}
          alt="Theme thumbnail"
          className="w-full h-48 object-cover rounded-lg shadow-md border border-gray-700"
        />

        <p className="mt-6 text-gray-100 text-lg font-medium truncate w-full">
          {theme.description.length > 60
            ? theme.description.slice(0, 57) + "..."
            : theme.description}
        </p>

        <p className="mt-2 text-sm text-gray-400">
          Downloads: {theme.downloads.toLocaleString()}
        </p>

        <button className="mt-4 flex items-center justify-center gap-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold px-4 py-2 rounded-3xl transition-all transform hover:scale-105 focus:ring-2 focus:ring-blue-400 focus:outline-none">
          <img src="/vscode.svg" alt="VS Code logo" className="w-6 h-6" />
          <span className="text-base font-medium">Install</span>
        </button>
      </div>
    </div>
  );
};
