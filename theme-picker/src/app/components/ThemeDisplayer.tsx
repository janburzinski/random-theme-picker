import Image from "next/image";
import { IDESelection } from "./ThemePicker";

export interface ThemeData {
  theme_name: string;
  description: string;
  install_link: string;
  last_update: string;
  author: string;
  extensionId: string;
  publisherId: string;
  previewImage: string;
}

type ThemeDisplayerProps = {
  theme: ThemeData;
  ide: IDESelection;
};

const demoPreviewImage =
  "https://raw.githubusercontent.com/Mofiqul/vscode.nvim/refs/heads/main/demo.png";

export const ThemeDisplayer: React.FC<ThemeDisplayerProps> = ({
  theme,
  ide,
}) => {
  console.log("theme:", theme);
  console.log("ide:", ide);
  return (
    <div className="flex justify-center items-center py-12">
      <div className="flex flex-col items-center bg-gradient-to-b from-gray-900 via-gray-800 to-black p-6 rounded-2xl shadow-xl max-w-md w-full text-center border border-gray-700">
        <Image
          src={theme.previewImage ? theme.previewImage : demoPreviewImage}
          alt="Theme thumbnail"
          width={50}
          height={50}
          className="w-full h-48 object-cover rounded-lg shadow-md border border-gray-700"
        />

        <p className="mt-6 text-gray-100 text-lg font-medium truncate w-full">
          {theme.description.length > 60
            ? theme.description.slice(0, 57) + "..."
            : theme.description}
        </p>

        <p className="mt-2 text-sm text-gray-400">Author: {theme.author}</p>

        <button className="mt-4 flex items-center justify-center gap-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold px-4 py-2 rounded-3xl transition-all transform hover:scale-105 focus:ring-2 focus:ring-blue-400 focus:outline-none">
          <Image
            src="/vscode.svg"
            alt="VS Code logo"
            width={50}
            height={50}
            className="w-6 h-6"
          />
          <span className="text-base font-medium">Install</span>
        </button>
      </div>
    </div>
  );
};
