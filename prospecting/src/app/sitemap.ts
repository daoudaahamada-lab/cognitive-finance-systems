import type { MetadataRoute } from "next";

const BASE = process.env.SITE_URL ?? "http://localhost:3000";

export default function sitemap(): MetadataRoute.Sitemap {
  return ["", "/mentions-legales", "/confidentialite", "/cgu"].map((path) => ({ url: `${BASE}${path}` }));
}
