/**
 * MCP Server for the Markdown Converter Power
 *
 * Registers the `convert_markdown` tool that converts Markdown content
 * to HTML, supporting GFM and CommonMark flavors.
 *
 * Uses @modelcontextprotocol/sdk for the MCP server implementation.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { convertMarkdown } from "./tools/markdown-converter.js";

const server = new McpServer({
  name: "markdown-converter",
  version: "0.1.0",
});

// Register the convert_markdown tool
server.tool(
  "convert_markdown",
  "Convert Markdown content to HTML. Supports GFM (GitHub Flavored Markdown) and CommonMark flavors.",
  {
    markdown: z.string().describe("Markdown content to convert"),
    flavor: z
      .enum(["gfm", "commonmark"])
      .optional()
      .describe("Markdown flavor: gfm (default) or commonmark"),
  },
  async ({ markdown, flavor }) => {
    try {
      const result = await convertMarkdown({ markdown, flavor });

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                html: result.html,
                flavor: result.flavor,
              },
              null,
              2
            ),
          },
        ],
      };
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unknown error occurred";
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({ error: message }),
          },
        ],
        isError: true,
      };
    }
  }
);

// Start the server using stdio transport
async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error("Server failed to start:", error);
  process.exit(1);
});
