"use client";

import Image from "next/image";
import { useState } from "react";
import { LoadingThemeAnimation } from "./LoadingTheme";
import { ThemeData, ThemeDisplayer } from "./ThemeDisplayer";

export type IDESelection = "vscode" | "jetbrains";

export const ThemePicker: React.FC = ({}) => {
  const [currentSelection, setCurrentSelection] =
    useState<IDESelection>("vscode");
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<ThemeData | null>(null);

  const jetBrainsLogo = "/jetbrains.svg";
  const vsCodeLogo = "/vscode.svg";

  const toastBoxStyle =
    currentSelection === "vscode"
      ? "relative bg-gradient-to-r from-purple-500 to-blue-500 text-white text-sm px-6 py-3 rounded-xl shadow-lg min-w-[50px] text-center"
      : "relative bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 text-white text-sm px-6 py-3 rounded-xl shadow-lg min-w-[50px] text-center";

  const handleLogoClick = () => {
    setCurrentSelection(currentSelection === "vscode" ? "jetbrains" : "vscode");
  };

  const pickRandomTheme = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`/api/get-theme/?ide=${currentSelection}`);
      if (!res.ok) throw new Error(`Error: ${res.status} | ${res.text}`);
      const json = await res.json();
      setData(json);
      console.log("data", data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }

    console.log(error);
  };

  return (
    <div className="relative flex flex-col items-center">
      <div className="">
        <div className="absolute -top-16 left-1/2 transform -translate-x-1/2 flex flex-col items-center">
          <div className={toastBoxStyle}>🙈</div>
          <div
            className="w-0 h-0 border-l-[10px] border-r-[10px] border-t-[10px] mt-[-1px]"
            style={{
              borderLeftColor: "transparent",
              borderRightColor: "transparent",
              borderTopColor: "rgba(107, 70, 193, 1)",
            }}
          ></div>
        </div>
        <Image
          src={currentSelection === "vscode" ? vsCodeLogo : jetBrainsLogo}
          alt="VS Code / JetBrains Logo"
          width={currentSelection === "vscode" ? 50 : 200}
          height={50}
          className="transition-transform cursor-pointer"
          onClick={handleLogoClick}
        />
      </div>

      <div className="text-4xl font-bold text-center">
        {isLoading && <LoadingThemeAnimation />}
        {!isLoading && data && (
          <ThemeDisplayer theme={data} ide={currentSelection} />
        )}
      </div>

      <button
        onClick={pickRandomTheme}
        className="mt-8 px-8 py-4 text-white bg-purple-500 rounded-3xl hover:bg-purple-600 transition-colors"
      >
        pick random theme
      </button>
    </div>
  );
};
