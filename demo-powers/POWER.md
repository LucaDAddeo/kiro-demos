# markdown-converter

A Kiro Power that converts Markdown content to HTML, supporting GitHub Flavored Markdown (GFM) and CommonMark flavors.

## Description

The markdown-converter power provides a single MCP tool that transforms Markdown text into HTML. It supports two flavors: GFM (with tables, strikethrough, and autolinks) and CommonMark (strict specification compliance).

## Keywords

- markdown
- html
- converter

## Tools

### convert_markdown

Convert Markdown content to HTML.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `markdown` | string | Yes | Markdown content to convert |
| `flavor` | `"gfm"` \| `"commonmark"` | No | Markdown flavor (default: `gfm`) |

**Returns:**

```json
{
  "html": "<h1>Hello</h1>\n<p>World</p>\n",
  "flavor": "gfm"
}
```

**Examples:**

Basic conversion:
```
Input:  { "markdown": "# Hello\n\nThis is **bold** text." }
Output: { "html": "<h1>Hello</h1>\n<p>This is <strong>bold</strong> text.</p>\n", "flavor": "gfm" }
```

With CommonMark flavor:
```
Input:  { "markdown": "~~strikethrough~~", "flavor": "commonmark" }
Output: { "html": "<p>~~strikethrough~~</p>\n", "flavor": "commonmark" }
```

GFM tables:
```
Input:  { "markdown": "| A | B |\n|---|---|\n| 1 | 2 |", "flavor": "gfm" }
Output: { "html": "<table><thead><tr><th>A</th><th>B</th></tr></thead><tbody><tr><td>1</td><td>2</td></tr></tbody></table>\n", "flavor": "gfm" }
```
