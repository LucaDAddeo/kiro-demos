# Serverless AI Assistant — Showcase End-to-End

> **Modalità di esecuzione:** Deployabile + Sviluppo locale  
> **Linguaggi:** Python 3.11  
> **Funzionalità Kiro:** Specs, Hooks, Steering

Un assistente AI serverless completo che dimostra come lo sviluppo spec-driven, gli hooks e i file di steering di Kiro lavorano insieme in un'applicazione AWS reale.

## Architettura

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Client    │────▶│  API Gateway     │────▶│  Lambda (Chat)  │
│  (HTTP)     │◀────│  (HTTP API)      │◀────│                 │
└─────────────┘     └──────────────────┘     └────────┬────────┘
                                                       │
                              ┌─────────────────────────┼──────────────────┐
                              │                         │                  │
                              ▼                         ▼                  ▼
                    ┌─────────────────┐     ┌─────────────────┐  ┌──────────────┐
                    │   DynamoDB      │     │  Amazon Bedrock  │  │   Lambda     │
                    │ (Conversations) │     │  (Claude)        │  │  (History)   │
                    └─────────────────┘     └─────────────────┘  └──────────────┘
```

**Componenti:**

- **API Gateway (HTTP API)** — Instrada le richieste alle funzioni Lambda con supporto CORS
- **Lambda (Chat)** — Riceve i messaggi utente, invoca Bedrock, salva le conversazioni
- **Lambda (History)** — Recupera la cronologia delle conversazioni per session ID
- **DynamoDB** — Memorizza i messaggi con session_id (PK) e timestamp (SK)
- **Amazon Bedrock** — Genera risposte AI utilizzando Claude Sonnet

## Funzionalità Kiro Utilizzate

### Specs (`.kiro/specs/assistant-api/`)

L'intero progetto è stato costruito seguendo il workflow spec di Kiro:

1. **requirements.md** — Definisce endpoint API, modelli dati e comportamento
2. **design.md** — Architettura tecnica, interfacce e gestione errori
3. **tasks.md** — Piano di implementazione con ID task referenziati nel codice sorgente

### Hooks (`.kiro/hooks/`)

- **test-on-save.json** — Esegue automaticamente i test quando i file Python cambiano (`fileEdited`)
- **security-check.json** — Valida le operazioni di scrittura per problemi di sicurezza (`preToolUse`)

### Steering (`.kiro/steering/`)

- **aws-best-practices.md** — Guida sempre attiva per l'uso dei servizi AWS (inclusione auto)
- **api-design.md** — Guida condizionale attivata quando si modificano i file handler API

## Struttura del Progetto

```
showcase-serverless-assistant/
├── .kiro/                    # Configurazione Kiro
│   ├── specs/assistant-api/  # Artefatti del workflow spec completo
│   ├── hooks/                # Hook di automazione
│   └── steering/             # Guida contestuale
├── src/
│   ├── handlers/             # Handler delle funzioni Lambda
│   ├── core/                 # Logica di business e modelli
│   └── utils/                # Utility AWS
├── tests/
│   ├── unit/                 # Test unitari per la logica core
│   └── integration/          # Test di integrazione (AWS mockato)
├── infra/
│   ├── template.yaml         # Template SAM
│   └── samconfig.toml        # Configurazione deploy SAM
├── local-dev.sh              # Script per sviluppo locale
├── teardown.sh               # Pulizia risorse AWS
└── COST-ESTIMATE.md          # Stima dei costi AWS
```

## Sviluppo Locale

### Prerequisiti

- Python 3.11+
- AWS SAM CLI (`pip install aws-sam-cli`)
- Docker (per SAM local)

### Setup

```bash
cd showcase-serverless-assistant

# Crea ambiente virtuale
python -m venv .venv
source .venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Esegui i test
pytest tests/ -v
```

### Esecuzione Locale con SAM

```bash
# Avvia API locale (richiede Docker)
./local-dev.sh

# Oppure manualmente:
sam local start-api --template infra/template.yaml --port 3000
```

L'API locale sarà disponibile su `http://localhost:3000`.

**Test degli endpoint:**

```bash
# Invia un messaggio chat
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Cos'\''è il serverless computing?"}'

# Ottieni la cronologia della conversazione
curl http://localhost:3000/history/{session_id}
```

## Deploy su AWS

### Prerequisiti

- AWS CLI configurato con credenziali appropriate
- SAM CLI installato
- Un account AWS con accesso ai modelli Bedrock abilitato

### Deploy

```bash
cd infra

# Build dell'applicazione
sam build

# Deploy (guidato per la prima volta)
sam deploy --guided

# Deploy successivi
sam deploy
```

Il deployment crea:
- Endpoint HTTP API Gateway
- Due funzioni Lambda (chat + history)
- Tabella DynamoDB (pay-per-request)
- Ruoli IAM con policy a privilegi minimi

### Configurazione

Modifica `infra/samconfig.toml` per personalizzare:
- Nome dello stack
- Regione AWS
- Ambiente (dev/staging/prod)

## Stima dei Costi

Vedi [COST-ESTIMATE.md](./COST-ESTIMATE.md) per il dettaglio dei prezzi.

**Riepilogo (uso dev/test):** ~$1–5/mese per uso leggero (< 1000 richieste/giorno).

## Teardown

Per rimuovere tutte le risorse AWS deployate ed evitare costi ricorrenti:

```bash
./teardown.sh
```

Oppure manualmente:

```bash
aws cloudformation delete-stack --stack-name assistant-dev
```

> **Importante:** La tabella DynamoDB verrà eliminata insieme a tutti i dati delle conversazioni. Esporta i dati necessari prima del teardown.

## Riferimento API

### POST /chat

Invia un messaggio e ricevi una risposta AI.

**Richiesta:**
```json
{
  "message": "La tua domanda qui",
  "session_id": "session-id-esistente-opzionale"
}
```

**Risposta (200):**
```json
{
  "response": "Risposta generata dall'AI",
  "session_id": "uuid-session-id",
  "timestamp": "2024-01-01T00:00:00+00:00"
}
```

### GET /history/{session_id}

Recupera la cronologia della conversazione per una sessione.

**Risposta (200):**
```json
{
  "session_id": "uuid-session-id",
  "messages": [
    {"role": "user", "content": "...", "timestamp": "..."},
    {"role": "assistant", "content": "...", "timestamp": "..."}
  ]
}
```

## Licenza

Questo progetto fa parte del repository kiro-ambassador-demos a scopo educativo.
