# Kiro: Lo Sviluppo Guidato dall'AI per AWS

**Formato:** Talk / Workshop  
**Durata:** 30 minuti  
**Target:** AWS User Group, community meetup, conferenze developer  
**Lingua:** Italiano  
**Materiale demo:** Repository `kiro-ambassador-demos`

---

## Scaletta della Presentazione

### 1. Introduzione (3 minuti)

**Contenuto:**
- Chi sono e perché parlo di Kiro
- Il problema: sviluppo software moderno è complesso, frammentato, e richiede context-switching continuo
- La promessa: un IDE che lavora *con* te, non solo *per* te
- Panoramica di cosa vedremo oggi

**Speaker Notes:**
> Iniziare con un aneddoto personale sullo sviluppo di un progetto AWS — quante volte si passa da documentazione a codice a terminale a browser. Kiro non è un altro copilot che autocompleta codice: è un ambiente di sviluppo che comprende il *contesto* del progetto e guida l'implementazione dall'inizio alla fine. Oggi vi mostro le funzionalità principali con demo live dal repository kiro-ambassador-demos.

---

### 2. Spec-Driven Development (5 minuti)

**Contenuto:**
- Il workflow: Requirements → Design → Tasks
- Come Kiro genera codice tracciabile alle specifiche
- Vantaggi: documentazione sempre aggiornata, decisioni architetturali esplicite
- Demo: mostrare `demo-specs/` — spec completa di un URL shortener

**Speaker Notes:**
> Lo spec-driven development è il cuore di Kiro. Invece di partire dal codice, si parte dai requisiti. Kiro genera un documento di design con architettura e interfacce, poi un piano di task granulare. Ogni riga di codice generata ha un commento che la collega al task di origine — tracciabilità totale. Mostrare il file `demo-specs/src/url_shortener.py` con i commenti `# Task X.Y` e come si collegano a `tasks.md`. Sottolineare che le spec non sono stubs — sono documenti completi e reali.

---

### 3. Hooks (5 minuti)

**Contenuto:**
- Cosa sono gli hooks: automazioni che reagiscono a eventi nell'IDE
- I quattro tipi di evento: `fileEdited`, `preToolUse`, `postToolUse`, `userTriggered`
- Esempi pratici: lint automatico, validazione sicurezza, generazione documentazione
- Demo: mostrare `demo-hooks/` — configurazione JSON e comportamento atteso

**Speaker Notes:**
> Gli hooks sono il sistema nervoso di Kiro. Pensateli come GitHub Actions, ma dentro l'IDE e in tempo reale. Quando salvi un file TypeScript, un hook può eseguire il linter. Quando Kiro sta per scrivere un file, un hook può validare che non ci siano problemi di sicurezza. Mostrare i quattro file JSON in `demo-hooks/.kiro/hooks/` e spiegare la struttura: eventType, hookAction, filePatterns/toolTypes. Enfatizzare che sono dichiarativi — non serve scrivere codice, solo configurazione.

---

### 4. Steering Files (4 minuti)

**Contenuto:**
- Cosa sono: file Markdown che forniscono contesto e linee guida all'agente AI
- Tre modalità di inclusione: auto (sempre attivo), conditional (match su file), manual (attivazione esplicita)
- Come personalizzare il comportamento di Kiro per il proprio progetto
- Demo: mostrare `demo-steering/` — frontmatter YAML e contenuto

**Speaker Notes:**
> I file di steering sono come dare istruzioni permanenti a un collega. "Quando lavori su file Python in questo progetto, segui sempre queste best practice AWS." La modalità auto è sempre attiva, conditional si attiva solo quando modifichi certi file (es. `**/*.py`), manual richiede attivazione esplicita. Mostrare il frontmatter YAML con `inclusion: conditional` e `globs: "**/*.py"`. Spiegare che è il modo per codificare le convenzioni del team.

---

### 5. Powers (MCP) (4 minuti)

**Contenuto:**
- Cosa sono i Powers: server MCP che estendono le capacità di Kiro
- Come creare un Power custom con tool personalizzati
- Esempio: convertitore Markdown → HTML come MCP tool
- Demo: mostrare `demo-powers/` — server TypeScript e POWER.md

**Speaker Notes:**
> I Powers sono il sistema di plugin di Kiro basato sul Model Context Protocol. Permettono di aggiungere tool esterni che l'agente può invocare. Nel nostro esempio, abbiamo un convertitore Markdown-to-HTML — semplice ma dimostra il pattern. In produzione potreste avere un Power che interroga il vostro database interno, genera diagrammi, o interagisce con API proprietarie. Mostrare `demo-powers/src/server.ts` e la registrazione del tool con inputSchema.

---

### 6. Integrazione con Agenti AI (4 minuti)

**Contenuto:**
- Tre pattern per agenti su AWS: Strands SDK, Bedrock Agents, AgentCore
- Come Kiro aiuta nello sviluppo di agenti (specs per definire comportamento, steering per best practice)
- Integrazione con cloud-ops-toolkit via submodule
- Demo: mostrare `demo-agents/strands-agent/` — agente con tool custom

**Speaker Notes:**
> Gli agenti AI sono il futuro dell'automazione cloud. Kiro supporta lo sviluppo di agenti con gli stessi strumenti visti prima: specs per definire cosa deve fare l'agente, hooks per testare automaticamente, steering per le best practice. Mostrare `demo-agents/strands-agent/agent.py` — un agente Strands che usa un tool custom collegato a cloud-ops-toolkit. Sottolineare che il toolkit non viene copiato ma referenziato via submodule — separazione delle responsabilità.

---

### 7. Live Demo: Showcase Project (3 minuti)

**Contenuto:**
- Presentare `showcase-serverless-assistant/` come progetto che unisce tutto
- Architettura: Lambda + API Gateway + DynamoDB + Bedrock
- Mostrare la directory `.kiro/` con specs, hooks e steering configurati insieme
- Esecuzione locale con `sam local start-api`

**Speaker Notes:**
> Questo è il progetto che mette tutto insieme. Un assistente AI serverless con API REST, persistenza delle conversazioni, e generazione di risposte via Bedrock. La directory `.kiro/` contiene specs complete (il progetto è stato costruito seguendo il workflow), hooks per test automatici e security check, e steering per best practice AWS. Se il tempo lo permette, fare una demo live con `sam local start-api` e una chiamata curl. Altrimenti mostrare la struttura e i test che passano.

---

### 8. Q&A e Risorse (2 minuti)

**Contenuto:**
- Link al repository: `github.com/your-username/kiro-ambassador-demos`
- Link alla documentazione Kiro
- Come iniziare: installare Kiro, aprire un progetto, creare la prima spec
- Contatti e community

**Speaker Notes:**
> Chiudere con i link pratici. Il repository è pubblico e contiene tutto quello che abbiamo visto oggi — ogni demo è isolata e può essere esplorata indipendentemente. Per iniziare con Kiro: installate l'IDE, aprite un progetto esistente, e provate a creare la vostra prima spec con il comando "Create Spec". La community è attiva su Discord e GitHub Discussions. Domande?

---

## Materiale Supplementare

### Slide Suggerite

1. **Titolo** — "Kiro: Lo Sviluppo Guidato dall'AI per AWS"
2. **Il Problema** — Diagramma del context-switching nello sviluppo moderno
3. **Spec Workflow** — Diagramma Requirements → Design → Tasks → Code
4. **Hooks** — Tabella dei 4 event types con esempi
5. **Steering** — Confronto delle 3 modalità di inclusione
6. **Powers** — Schema MCP client ↔ server
7. **Agenti** — Architettura dei 3 pattern (Strands, Bedrock Agents, AgentCore)
8. **Showcase** — Diagramma architetturale del serverless assistant
9. **Risorse** — QR code al repository + link utili

### Demo Checklist

- [ ] Repository clonato e aggiornato
- [ ] Python 3.11+ installato con dipendenze
- [ ] Docker running (per SAM local)
- [ ] SAM CLI installato
- [ ] Terminale pronto con directory corretta
- [ ] Browser aperto su Kiro docs come backup

### Adattamenti per Workshop (60+ minuti)

Se il formato è workshop anziché talk:

1. **Hands-on spec creation** (15 min) — I partecipanti creano una spec per un progetto semplice
2. **Hook configuration** (10 min) — Configurare un hook personalizzato
3. **Local deployment** (10 min) — Deploy locale del showcase con SAM
4. **Q&A esteso** (10 min) — Discussione su casi d'uso specifici dei partecipanti
