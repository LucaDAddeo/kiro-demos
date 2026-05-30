# Demo: MCP Powers

> **Modalità di esecuzione:** solo locale — non richiede account AWS né connessione di rete

Questa demo mostra i **Kiro Powers** — server MCP (Model Context Protocol) personalizzati che estendono Kiro con nuovi strumenti e capacità. I Powers permettono di dare all'agente AI accesso a servizi esterni, logica personalizzata o funzionalità specializzate attraverso un protocollo standardizzato.

## Cosa Sono i MCP Powers?

Un MCP Power è un server che implementa il Model Context Protocol, esponendo **tool** che l'agente AI di Kiro può invocare. Ogni power è un pacchetto autonomo con:

- **`POWER.md`** — Documentazione che descrive i tool del power, parametri e utilizzo
- **Implementazione server** — Il server MCP che gestisce le richieste dei tool
- **Definizioni dei tool** — Funzioni che l'agente AI può chiamare con parametri tipizzati

Una volta installato, Kiro scopre i tool del power e li rende disponibili all'agente durante le conversazioni.

## Questa Demo: Markdown Converter

Questo power fornisce un tool `convert_markdown` che trasforma contenuto Markdown in HTML, supportando due varianti:

| Variante | Descrizione |
|----------|-------------|
| `gfm` (default) | GitHub Flavored Markdown — tabelle, barrato, autolink |
| `commonmark` | Conformità stretta alla specifica CommonMark |

### Tool: `convert_markdown`

| Parametro | Tipo | Obbligatorio | Descrizione |
|-----------|------|--------------|-------------|
| `markdown` | string | Sì | Contenuto Markdown da convertire |
| `flavor` | `"gfm"` \| `"commonmark"` | No | Variante Markdown (default: `gfm`) |

**Esempio di utilizzo:**

```json
{
  "markdown": "# Hello World\n\nQuesto è **grassetto** e ~~barrato~~.",
  "flavor": "gfm"
}
```

**Risposta:**

```json
{
  "html": "<h1>Hello World</h1>\n<p>Questo è <strong>grassetto</strong> e <del>barrato</del>.</p>\n",
  "flavor": "gfm"
}
```

## Setup

```bash
# Installa le dipendenze
npm install

# Compila il sorgente TypeScript
npm run build

# Avvia il server MCP (trasporto stdio)
npm start
```

### Modalità sviluppo

```bash
# Osserva le modifiche e ricompila
npm run dev
```

## Struttura del Progetto

```
demo-powers/
├── POWER.md                        # Documentazione del power (definizioni tool)
├── src/
│   ├── server.ts                   # Setup server MCP e registrazione tool
│   └── tools/
│       └── markdown-converter.ts   # Implementazione del tool
├── package.json                    # Dipendenze con versioni fissate
├── tsconfig.json                   # Configurazione TypeScript
├── .env.example                    # Template variabili d'ambiente
├── README.md
└── README.it.md
```

## Come Funziona

### 1. Registrazione del Server

Il server MCP si registra con un nome e una versione:

```typescript
const server = new McpServer({
  name: "markdown-converter",
  version: "0.1.0",
});
```

### 2. Definizione del Tool

I tool vengono registrati con un nome, una descrizione e uno schema di parametri tipizzato:

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
    // Implementazione del tool
  }
);
```

### 3. Trasporto

Il server comunica tramite trasporto stdio, che Kiro usa per inviare richieste e ricevere risposte:

```typescript
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Dipendenze

| Pacchetto | Versione | Scopo |
|-----------|----------|-------|
| `@modelcontextprotocol/sdk` | 1.12.1 | Framework server MCP |
| `marked` | 15.0.4 | Conversione Markdown-to-HTML |
| `typescript` | 5.7.3 | Compilatore TypeScript (dev) |

## Creare il Proprio Power

1. Inizializza un nuovo progetto TypeScript con `@modelcontextprotocol/sdk`
2. Crea un `POWER.md` che documenta i tuoi tool
3. Implementa il server MCP con le registrazioni dei tool
4. Compila e testa localmente con `npm run build && npm start`
5. Installa in Kiro puntando alla directory del tuo power
