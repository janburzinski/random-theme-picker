import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  images: {
    domains: [
      "github.com",
      "raw.githubusercontent.com",
      "downloads.marketplace.jetbrains.com",
    ],
  },
};

export default nextConfig;
