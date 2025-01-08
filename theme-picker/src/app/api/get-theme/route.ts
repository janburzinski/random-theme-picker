import { NextApiRequest, NextApiResponse } from "next";
import { NextResponse } from "next/server";

const jetBrainsThemes =
  "https://raw.githubusercontent.com/janburzinski/random-theme-picker/refs/heads/main/themes-loader/jetbrains_themes.json";
const vsCodeThemes =
  "https://raw.githubusercontent.com/janburzinski/random-theme-picker/refs/heads/main/themes-loader/vscode_themes.json";

export async function GET(req: NextApiRequest, res: NextApiResponse) {
  if (!req.url)
    return NextResponse.json(
      { error: "invalid request: missing url " },
      { status: 400 }
    );

  const url = new URL(req.url!);
  const ide = url.searchParams.get("ide");
  const availableIDEs = ["vscode", "jetbrains"];

  if (typeof ide !== "string" || !availableIDEs.includes(ide))
    return NextResponse.json(
      { error: "invalid ide provided" },
      { status: 400 }
    );

  //fetch data and pick random theme
  const data = await getAvailableThemes(ide);
  if (!data)
    return NextResponse.json(
      { error: "invalid ide provided" },
      { status: 400 }
    );

  const randomIndex = Math.floor(Math.random() * data.length);
  return NextResponse.json(data[randomIndex]);
}

interface ThemeData {
  theme_name: string;
  description: string;
  install_link: string;
  last_update: string;
  author: string;
  extensionId: string;
  publisherId: string;
  previewImage: string;
}

const getAvailableThemes = async (ide: string): Promise<ThemeData[]> => {
  const themeUrl = ide === "vscode" ? vsCodeThemes : jetBrainsThemes;
  console.log(themeUrl);
  const response = await fetch(themeUrl);
  if (!response.ok) throw new Error("failed to fetch themes");
  const themes: ThemeData[] = await response.json();
  return themes;
};
