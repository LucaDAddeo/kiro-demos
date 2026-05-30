# Demo Agent Workflows

**Modalità di esecuzione:** Deployable

Questa demo presenta tre pattern di sviluppo di agenti AI su AWS, ciascuno integrato con [cloud-ops-toolkit](https://github.com/your-org/cloud-ops-toolkit) per l'automazione operativa.

## Pattern degli Agenti

### 1. Strands Agents SDK (`strands-agent/`)

Un agente Python costruito con [Strands Agents SDK](https://github.com/strands-agents/sdk-python) utilizzando Amazon Bedrock come provider del modello.

**Architettura:**
```
Prompt Utente → Strands Agent → BedrockModel (Claude)
                     ↓
              tool analyze_costs
                     ↓
       cloud-ops-toolkit/scripts/finops/cost-analysis.sh
```

- `agent.py` — Inizializzazione dell'agente con BedrockModel
- `tools.py` — Tool personalizzato `analyze_costs` che invoca cloud-ops-toolkit via subprocess
- `requirements.txt` — Dipendenze con versioni fissate

### 2. Bedrock Agents (`bedrock-agent/`)

Un agente gestito tramite Amazon Bedrock Agents con un action group supportato da Lambda.

**Architettura:**
```
Utente → Bedrock Agent → Action Group (Lambda)
                              ↓
                     AnalyzeCosts / ListResources
                              ↓
                     Cost Explorer / Resource Groups API
```

- `action_group.py` — Handler Lambda che elabora le richieste dell'action group
- `agent-schema.json` — Schema OpenAPI che definisce l'API dell'action group
- `requirements.txt` — Dipendenze con versioni fissate

### 3. AgentCore Deployment (`agentcore-deploy/`)

Configurazione di deployment per Amazon Bedrock AgentCore, che fornisce infrastruttura gestita per l'esecuzione degli agenti.

**Architettura:**
```
AgentCore Runtime → Agent Handler → Invocazioni Tool
       ↓                                    ↓
  Memoria Sessione              script cloud-ops-toolkit
```

- `agent_config.yaml` — Configurazione di deployment AgentCore (modello, tool, memoria, guardrail)
- `runtime/handler.py` — Handler runtime dell'agente per l'elaborazione delle richieste

## Integrazione con Cloud-Ops-Toolkit

I tool dell'agente invocano gli script di cloud-ops-toolkit via subprocess anziché duplicarli. Configura il toolkit come submodule Git:

```bash
# Dalla root del repository
git submodule add https://github.com/your-org/cloud-ops-toolkit.git cloud-ops-toolkit
git submodule update --init

# Oppure imposta il percorso tramite variabile d'ambiente
export CLOUD_OPS_TOOLKIT_PATH=../cloud-ops-toolkit
```

Consulta [cloud-ops-toolkit/docs/integrations.md](../cloud-ops-toolkit/docs/integrations.md) per la documentazione completa sui pattern di integrazione.

## Permessi IAM Richiesti

L'agente richiede i seguenti permessi (vedi `iam-policies/agent-execution-role.json`):

| Permesso | Risorsa | Scopo |
|----------|---------|-------|
| `bedrock:InvokeModel` | `arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-*` | Inferenza del modello |
| `bedrock:CreateAgent`, `bedrock:InvokeAgent` | `arn:aws:bedrock:us-east-1:123456789012:agent/*` | Gestione agente |
| `lambda:InvokeFunction` | `arn:aws:lambda:us-east-1:123456789012:function:demo-agents-*` | Esecuzione action group |
| `ce:GetCostAndUsage` | `*` | Analisi dei costi |
| `tag:GetResources` | `*` | Elenco risorse |

> **Nota:** Tutti gli ARN utilizzano l'account ID placeholder `123456789012`. Sostituisci con il tuo account ID reale prima del deployment.

## Setup

### Prerequisiti

- Python 3.11+
- AWS CLI configurato con un profilo nominato
- AWS SAM CLI (per il deployment)
- cloud-ops-toolkit clonato come submodule

### Installazione

```bash
# Installa le dipendenze per l'agente Strands
cd strands-agent
pip install -r requirements.txt

# Configura l'ambiente
cp ../.env.example .env
# Modifica .env con il tuo profilo AWS e la regione
```

### Test Locale (Strands Agent)

```bash
cd strands-agent
export AWS_PROFILE=your-profile-name
export AWS_REGION=us-east-1
python agent.py
```

## Deployment

### Deploy tramite SAM

```bash
cd infra

# Build del pacchetto Lambda
sam build

# Deploy (prima volta — guidato)
sam deploy --guided

# Deploy successivi
sam deploy --profile your-profile-name
```

### Configurazione

Modifica `infra/samconfig.toml` per personalizzare:
- `stack_name` — Nome dello stack CloudFormation
- `region` — Regione AWS di destinazione
- `profile` — Profilo AWS CLI
- `parameter_overrides` — Ambiente (dev/staging/prod)

## Stima dei Costi

Consulta [COST-ESTIMATE.md](./COST-ESTIMATE.md) per la stima dei costi AWS.

**Riepilogo:** $5–25/mese per un utilizzo a livello demo (principalmente costi di inferenza Bedrock).

## Teardown

Rimuovi tutte le risorse AWS deployate per interrompere gli addebiti:

```bash
./teardown.sh
```

Oppure manualmente:

```bash
cd infra
sam delete --stack-name demo-agents-stack --profile your-profile-name --no-prompts
```
