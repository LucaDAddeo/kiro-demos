# MCP Powers Demo

> **Execution mode:** local-only — no AWS account or network required

This demo showcases **Kiro Powers** — custom MCP (Model Context Protocol) servers that extend Kiro with new tools and capabilities. Powers let you give the AI agent access to external services, custom logic, or specialized functionality through a standardized protocol.

## What Are MCP Powers?

An MCP Power is a server that implements the Model Context Protocol, exposing **tools** that Kiro's AI agent can invoke. Each power is a self-contained package with:

- **`POWER.md`** — Documentation describing the power's tools, parameters, and usage
- **Server implementation** — The MCP server that handles tool requests
- **Tool definitions** — Functions the AI agent can call with typed parameters

When installed, Kiro discovers the power's tools and makes them available to the agent during conversations.

## This Demo: Markdown Converter

This power provides a `convert_markdown` tool that transforms Markdown content into HTML, supporting two flavors:

| Flavor | Description |
|--------|-------------|
| `gfm` (default) | GitHub Flavored Markdown — tables, strikethrough, autolinks |
| `commonmark` | Strict CommonMark specification compliance |

### Tool: `convert_markdown`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `markdown` | string | Yes | Markdown content to convert |
| `flavor` | `"gfm"` \| `"commonmark"` | No | Markdown flavor (default: `gfm`) |

**Example usage:**

```json
{
  "markdown": "# Hello World\n\nThis is **bold** and ~~struck~~.",
  "flavor": "gfm"
}
```

**Response:**

```json
{
  "html": "<h1>Hello World</h1>\n<p>This is <strong>bold</strong> and <del>struck</del>.</p>\n",
  "flavor": "gfm"
}
```

## Setup

```bash
# Install dependencies
npm install

# Build the TypeScript source
npm run build

# Start the MCP server (stdio transport)
npm start
```

### Development mode

```bash
# Watch for changes and rebuild
npm run dev
```

## Project Structure

```
demo-powers/
├── POWER.md                        # Power documentation (tool definitions)
├── src/
│   ├── server.ts                   # MCP server setup and tool registration
│   └── tools/
│       └── markdown-converter.ts   # Tool implementation
├── package.json                    # Pinned dependencies
├── tsconfig.json                   # TypeScript configuration
├── .env.example                    # Environment variable template
├── README.md
└── README.it.md
```

## How It Works

### 1. Server Registration

The MCP server registers itself with a name and version:

```typescript
const server = new McpServer({
  name: "markdown-converter",
  version: "0.1.0",
});
```

### 2. Tool Definition

Tools are registered with a name, description, and typed parameter schema:

```typescript
server.tool(
  "convert_markdown",
  "Convert Markdown content to HTML",
  {
    markdown: z.string().describe("Markdown content to convert"),
    flavor: z.enum(["gfm", "commonmark"]).optional()
      .describe("Markdown flavor: gfm (default) or commonmark"),
  },
  async ({ markdown, flavor }) => {
    // Tool implementation
  }
);
```

### 3. Transport

The server communicates via stdio transport, which Kiro uses to send requests and receive responses:

```typescript
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `@modelcontextprotocol/sdk` | 1.12.1 | MCP server framework |
| `marked` | 15.0.4 | Markdown-to-HTML conversion |
| `typescript` | 5.7.3 | TypeScript compiler (dev) |

## Creating Your Own Power

1. Initialize a new TypeScript project with `@modelcontextprotocol/sdk`
2. Create a `POWER.md` documenting your tools
3. Implement the MCP server with tool registrations
4. Build and test locally with `npm run build && npm start`
5. Install in Kiro by pointing to your power's directory
