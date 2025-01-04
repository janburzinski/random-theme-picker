"use client";

import { useEffect, useState } from "react";

export const LoadingThemeAnimation: React.FC = ({}) => {
  const emojis = ["😀", "🎉", "🚀", "🌟", "🐱", "🍕", "🎨", "🌍", "🔥", "✨"];
  const [currentEmojiIndex, setCurrentEmojiIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentEmojiIndex((prevIndex) => (prevIndex + 1) % emojis.length);
    }, 700);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-center justify-center min-h-[50px]">
      <span
        className="text-2xl sm:text-3xl md:text-4xl transition-opacity duration-500 ease-in-out opacity-100"
        key={currentEmojiIndex}
      >
        {emojis[currentEmojiIndex]}
      </span>
      <h1>picking random theme...</h1>
    </div>
  );
};
