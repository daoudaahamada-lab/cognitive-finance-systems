import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  typedRoutes: false,
  serverExternalPackages: ["@prisma/client", "playwright-core"],
};

export default nextConfig;
