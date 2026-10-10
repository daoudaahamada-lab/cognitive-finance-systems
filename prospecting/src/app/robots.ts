import type { MetadataRoute } from "next";

const BASE = process.env.SITE_URL ?? "http://localhost:3000";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", allow: "/", disallow: ["/dashboard", "/inbox", "/campaigns", "/prospects", "/meetings", "/accounts", "/settings", "/api"] },
    sitemap: `${BASE}/sitemap.xml`,
  };
}
