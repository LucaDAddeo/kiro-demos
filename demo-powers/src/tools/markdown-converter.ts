/**
 * Markdown Converter Tool
 *
 * Converts Markdown content to HTML using the `marked` library.
 * Supports GFM (GitHub Flavored Markdown) and CommonMark flavors.
 */

import { marked, type MarkedOptions } from "marked";

export type MarkdownFlavor = "gfm" | "commonmark";

export interface ConvertOptions {
  markdown: string;
  flavor?: MarkdownFlavor;
}

export interface ConvertResult {
  html: string;
  flavor: MarkdownFlavor;
}

/**
 * Configure marked options based on the selected flavor.
 */
function getMarkedOptions(flavor: MarkdownFlavor): MarkedOptions {
  if (flavor === "gfm") {
    return {
      gfm: true,
      breaks: false,
    };
  }

  // CommonMark: disable GFM extensions
  return {
    gfm: false,
    breaks: false,
  };
}

/**
 * Convert Markdown content to HTML.
 *
 * @param options - The markdown content and optional flavor selection.
 * @returns The converted HTML and the flavor used.
 */
export async function convertMarkdown(
  options: ConvertOptions
): Promise<ConvertResult> {
  const flavor: MarkdownFlavor = options.flavor ?? "gfm";
  const markedOptions = getMarkedOptions(flavor);

  const html = await marked(options.markdown, markedOptions);

  return {
    html: html as string,
    flavor,
  };
}
