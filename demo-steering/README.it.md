# Demo: Steering Files

> **Modalità di esecuzione:** solo locale — non richiede account AWS né connessione di rete

Questa demo mostra i **Kiro steering files** — documenti Markdown che guidano il comportamento dell'agente AI con contesto specifico del progetto, standard di codifica e conoscenza di dominio. Gli steering files modellano il modo in cui Kiro scrive codice, revisiona modifiche e prende decisioni all'interno del tuo progetto.

## Cosa Sono gli Steering Files?

Uno steering file è un documento Markdown posizionato in `.kiro/steering/` che fornisce guida contestuale all'agente AI. Ogni file ha un blocco frontmatter YAML che controlla **quando** la guida viene attivata:

```markdown
---
inclusion: auto | conditional | manual
globs: "**/*.py"          # Solo per la modalità conditional
description: "Breve descrizione di quando questa guida si applica"
---

# Il contenuto della tua guida qui
```

## Modalità di Inclusione

Kiro supporta tre modalità di inclusione, ciascuna adatta a diversi casi d'uso:

---

### 1. Auto (Sempre Attiva): `code-style.md`

```yaml
---
inclusion: auto
description: "Always-on coding style guidelines applied to all files in the project"
---
```

**Quando si attiva:** Sempre. Questa guida è inclusa in ogni interazione con l'agente AI, indipendentemente dal file su cui stai lavorando.

**Caso d'uso:** Standard universali del progetto — convenzioni di naming, requisiti di documentazione, pattern di gestione errori e regole di organizzazione del codice.

**Contenuto di esempio in questa demo:**
- `snake_case` per Python, `camelCase` per TypeScript
- Docstring in stile Google obbligatorie per tutte le funzioni pubbliche
- Type hints obbligatori su tutte le firme di funzione
- Nessun `except:` generico — catturare sempre eccezioni specifiche

📄 `.kiro/steering/code-style.md`

---

### 2. Conditional (Condizionale): `aws-patterns.md`

```yaml
---
inclusion: conditional
globs: "**/*.py"
description: "AWS best practices applied when working with Python files that interact with AWS services"
---
```

**Quando si attiva:** Solo quando stai lavorando su file che corrispondono al pattern `globs`. In questo caso, qualsiasi file Python (`.py`) attiva la guida sui pattern AWS.

**Caso d'uso:** Guida specifica per dominio rilevante solo per certi tipi di file — pattern AWS SDK per file Python, pattern React per file `.tsx`, pattern database per file di migrazione.

**Contenuto di esempio in questa demo:**
- Gestione esplicita delle sessioni boto3 (nessuna sessione di default)
- Usare sempre i paginator per le chiamate API AWS
- Configurazione retry botocore con modalità adattiva
- Catturare eccezioni AWS specifiche usando le eccezioni del client

📄 `.kiro/steering/aws-patterns.md`

---

### 3. Manual (Manuale): `migration-guide.md`

```yaml
---
inclusion: manual
description: "Migration guide for upgrading from v1 to v2 API — activate manually when performing migration work"
---
```

**Quando si attiva:** Solo quando lo attivi esplicitamente dall'interfaccia di Kiro. L'agente non carica questa guida automaticamente.

**Caso d'uso:** Guida temporanea o situazionale — guide di migrazione, istruzioni di refactoring una tantum, convenzioni specifiche per sprint, o pattern sperimentali che vuoi provare selettivamente.

**Contenuto di esempio in questa demo:**
- Breaking changes tra API v1 e v2
- Istruzioni di migrazione passo-passo
- Piano di rollback in caso di problemi

📄 `.kiro/steering/migration-guide.md`

---

## Struttura del Progetto

```
demo-steering/
├── .kiro/
│   └── steering/
│       ├── code-style.md           # inclusion: auto (sempre attiva)
│       ├── aws-patterns.md         # inclusion: conditional (file Python)
│       └── migration-guide.md      # inclusion: manual (attivata dall'utente)
├── examples/
│   └── sample-project/
│       └── lambda_handler.py       # Attiva lo steering condizionale
├── README.md
└── README.it.md
```

## Creare Steering Files Personalizzati

### Passo 1: Crea il file

Crea un nuovo file `.md` nella directory `.kiro/steering/` del tuo progetto:

```bash
mkdir -p .kiro/steering
touch .kiro/steering/my-guidelines.md
```

### Passo 2: Aggiungi il frontmatter

Scegli la modalità di inclusione appropriata:

```markdown
---
inclusion: auto
description: "Le mie linee guida per tutto il progetto"
---
```

Oppure per attivazione condizionale:

```markdown
---
inclusion: conditional
globs: "src/**/*.ts"
description: "Pattern TypeScript per la directory src"
---
```

### Passo 3: Scrivi la tua guida

Aggiungi istruzioni chiare e attuabili in Markdown. Usa intestazioni, esempi di codice e elenchi puntati:

```markdown
# Le Mie Linee Guida

## Convenzioni di Naming
- Usa nomi di variabili descrittivi
- Prefissa le interfacce con `I`

## Esempi di Codice
\```python
# Corretto
def calculate_total(items: list[Item]) -> Decimal:
    ...

# Errato
def calc(x):
    ...
\```
```

### Passo 4: Kiro lo attiva automaticamente

Una volta salvato, Kiro rileva lo steering file e lo applica secondo la sua modalità di inclusione. Non serve riavvio né configurazione aggiuntiva.

## Suggerimenti

- Mantieni gli steering files focalizzati — un argomento per file
- Usa `auto` con parsimonia per evitare sovraccarico di contesto
- `conditional` con globs specifici è la modalità più efficiente per progetti grandi
- Aggiorna gli steering files man mano che il progetto evolve — sono documenti vivi
