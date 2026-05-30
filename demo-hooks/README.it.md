# Demo: Hooks

> **Modalità di esecuzione:** solo locale — non richiede account AWS né connessione di rete

Questa demo mostra i **Kiro hooks** — automazioni che attivano azioni dell'agente in base a eventi dell'IDE. Gli hooks permettono di applicare standard di codifica, validare operazioni, revisionare output ed eseguire script automaticamente, senza intervento manuale.

## Cosa Sono i Kiro Hooks?

Un hook è una configurazione JSON che mappa un evento dell'IDE a un'azione automatizzata. Quando l'evento specificato si verifica, Kiro esegue l'azione configurata — eseguendo un comando shell o chiedendo all'agente AI di svolgere un compito.

```json
{
  "id": "hook-id",
  "name": "Nome Leggibile",
  "description": "Cosa fa questo hook",
  "eventType": "fileEdited | preToolUse | postToolUse | userTriggered",
  "hookAction": "runCommand | askAgent"
}
```

## Esempi di Hook

Questa demo include quattro hook che coprono tutti i principali tipi di evento:

---

### 1. Lint al Salvataggio (`lint-on-save`)

| Proprietà | Valore |
|-----------|--------|
| **Tipo Evento** | `fileEdited` |
| **Tipo Azione** | `runCommand` |
| **Pattern File** | `**/*.ts` |
| **Comando** | `npx eslint --fix {file}` |

**Condizione di attivazione:** Un qualsiasi file TypeScript (`.ts`) viene salvato nel progetto.

**Risultato atteso:** ESLint viene eseguito automaticamente con auto-fix sul file salvato, garantendo uno stile di codice consistente senza linting manuale.

---

### 2. Validazione Operazioni di Scrittura (`validate-write`)

| Proprietà | Valore |
|-----------|--------|
| **Tipo Evento** | `preToolUse` |
| **Tipo Azione** | `askAgent` |
| **Tipi Tool** | `write` |
| **Prompt Agente** | Verifica conformità agli standard di codifica prima di procedere |

**Condizione di attivazione:** L'agente AI sta per eseguire un'operazione di scrittura (creazione o modifica di un file).

**Risultato atteso:** L'agente revisiona la scrittura in sospeso per convenzioni di naming, gestione errori, segreti hardcoded e documentazione prima che l'operazione venga eseguita. I problemi vengono segnalati prima che il codice venga scritto.

---

### 3. Revisione Output del Tool (`review-output`)

| Proprietà | Valore |
|-----------|--------|
| **Tipo Evento** | `postToolUse` |
| **Tipo Azione** | `askAgent` |
| **Tipi Tool** | `write` |
| **Prompt Agente** | Revisiona il risultato dell'esecuzione per bug, problemi di sicurezza e deviazioni dall'architettura |

**Condizione di attivazione:** L'agente AI ha appena completato un'operazione di scrittura.

**Risultato atteso:** L'agente revisiona il risultato per bug introdotti, gestione errori mancante, problemi di sicurezza o deviazioni dall'architettura del progetto. Vengono suggeriti miglioramenti se necessario.

---

### 4. Generazione Documentazione (`generate-docs`)

| Proprietà | Valore |
|-----------|--------|
| **Tipo Evento** | `userTriggered` |
| **Tipo Azione** | `runCommand` |
| **Comando** | `python scripts/generate-docs.py` |

**Condizione di attivazione:** L'utente attiva manualmente questo hook dall'interfaccia di Kiro.

**Risultato atteso:** Lo script di generazione documentazione viene eseguito, aggiornando la documentazione del progetto a partire dai commenti e docstring del codice sorgente.

---

## Struttura del Progetto

```
demo-hooks/
├── .kiro/
│   └── hooks/
│       ├── lint-on-save.json       # fileEdited → runCommand
│       ├── validate-write.json     # preToolUse → askAgent
│       ├── review-output.json      # postToolUse → askAgent
│       └── generate-docs.json      # userTriggered → runCommand
├── examples/
│   ├── sample-file.ts              # File trigger per la demo fileEdited
│   └── expected-output.md          # Documentazione comportamento atteso
├── .env.example
├── README.md
└── README.it.md
```

## Riferimento Configurazione Hook

### Campi Obbligatori (tutti gli hook)

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | string | Identificatore in kebab-case |
| `name` | string | Titolo leggibile |
| `description` | string | Cosa fa l'hook |
| `eventType` | string | Evento che attiva l'hook |
| `hookAction` | string | `askAgent` o `runCommand` |

### Campi Condizionali

| Campo | Richiesto Quando | Descrizione |
|-------|-----------------|-------------|
| `filePatterns` | `eventType: "fileEdited"` | Pattern glob separati da virgola (es. `**/*.ts, **/*.py`) |
| `toolTypes` | `eventType: "preToolUse"` o `"postToolUse"` | Filtro categoria tool (es. `write`, `read`, `shell`) |
| `outputPrompt` | `hookAction: "askAgent"` | Istruzione per l'agente AI |
| `command` | `hookAction: "runCommand"` | Comando shell da eseguire |

## Creare i Propri Hook

1. Crea un file JSON in `.kiro/hooks/` con un nome descrittivo
2. Definisci il tipo di evento che deve attivare l'hook
3. Scegli l'azione: `runCommand` per script, `askAgent` per revisione AI
4. Aggiungi i campi condizionali richiesti in base al tipo di evento
5. Kiro rileverà e attiverà automaticamente l'hook
