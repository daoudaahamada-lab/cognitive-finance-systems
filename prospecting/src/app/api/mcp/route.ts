import { WebStandardStreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js";
import { buildMcpServer } from "@/server/mcp/server";
import { authenticateToken } from "@/server/services/tokens";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

function unauthorized(description: string): Response {
  return Response.json(
    { error: "invalid_token", error_description: description },
    { status: 401, headers: { "WWW-Authenticate": `Bearer realm="vela", error="invalid_token"` } },
  );
}

/**
 * MCP over Streamable HTTP, stateless: each request gets its own server bound to
 * the workspace of the personal access token (Authorization: Bearer vela_...).
 */
async function handle(request: Request): Promise<Response> {
  const token = /^Bearer\s+(\S+)$/i.exec(request.headers.get("authorization") ?? "")?.[1];
  if (!token) return unauthorized("Ajoutez l'en-tête Authorization: Bearer <jeton> (jeton créé dans Réglages → Accès MCP).");
  const identity = await authenticateToken(token);
  if (!identity) return unauthorized("Jeton inconnu ou révoqué.");

  const server = buildMcpServer(identity);
  const transport = new WebStandardStreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
  await server.connect(transport);
  const response = await transport.handleRequest(request, { authInfo: { token, clientId: identity.tokenId, scopes: [] } });
  // JSON mode: the response is fully built once handleRequest resolves.
  await server.close();
  return response;
}

export { handle as GET, handle as POST, handle as DELETE };
