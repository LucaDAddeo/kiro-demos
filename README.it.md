# Kiro Ambassador Demos

Repository dimostrativo multi-linguaggio che presenta le funzionalità di [Kiro IDE](https://kiro.dev) per il programma Kiro Ambassador. Ogni cartella demo isola una singola funzionalità di Kiro con esempi funzionanti che puoi esplorare, modificare e da cui imparare.

---

## Indice

| Cartella | Funzionalità | Modalità | Linguaggio |
|----------|-------------|----------|------------|
| [`demo-specs/`](demo-specs/) | Sviluppo guidato da spec | solo locale | Python |
| [`demo-hooks/`](demo-hooks/) | Automazione con hooks | solo locale | Bash/JSON |
| [`demo-steering/`](demo-steering/) | File di steering | solo locale | Markdown |
| [`demo-powers/`](demo-powers/) | MCP Powers | solo locale | TypeScript |
| [`demo-agents/`](demo-agents/) | Workflow con agenti | deployabile | Python |
| [`showcase-serverless-assistant/`](showcase-serverless-assistant/) | Showcase end-to-end | deployabile | Python |

Le demo **solo locale** funzionano interamente sulla tua macchina senza necessità di un account AWS o connessione di rete.  
Le demo **deployabili** includono infrastruttura AWS (SAM/CDK) e forniscono stime dei costi e script di teardown.

---

## Relazione con cloud-ops-toolkit

Questo repository e [cloud-ops-toolkit](https://github.com/lucadaddeo/cloud-ops-toolkit) hanno scopi complementari:

| Aspetto | cloud-ops-toolkit | kiro-ambassador-demos |
|---------|-------------------|----------------------|
| Scopo | Script Bash production-ready per operazioni AWS | Demo educative delle funzionalità di Kiro IDE |
| Linguaggio | Esclusivamente Bash | Python, TypeScript, Bash |
| Pubblico | Ingegneri DevOps | Sviluppatori che imparano Kiro |
| Integrazione | Script autonomi | Riferimento al toolkit come Git submodule |

Le demo dei workflow con agenti invocano gli script di cloud-ops-toolkit tramite subprocess — non li duplicano mai. Se hai bisogno del toolkit in locale, la cartella `demo-agents/` include la configurazione del submodule per scaricarlo.

---

## Prerequisiti

- [Kiro IDE](https://kiro.dev) (ultima versione)
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) (per le demo deployabili)
- Python 3.11+
- Node.js 18+
- [jq](https://jqlang.github.io/jq/) (elaborazione JSON)

---

## Avvio Rapido

```bash
# Clona il repository
git clone https://github.com/your-username/kiro-ambassador-demos.git
cd kiro-ambassador-demos

# Inizializza i submodule (per le demo degli agenti che referenziano cloud-ops-toolkit)
git submodule update --init --recursive

# Installa i pre-commit hook per la scansione dei segreti
pip install pre-commit
pre-commit install

# Esplora una demo solo locale
cd demo-specs
pip install -r requirements.txt
python src/url_shortener.py --help
```

Per le demo deployabili, configura prima il tuo profilo AWS:

```bash
export AWS_PROFILE=your-profile-name
cd demo-agents
sam build && sam deploy --guided
```

---

## Struttura del Repository

```
kiro-ambassador-demos/
├── README.md                          # Documentazione in inglese
├── README.it.md                       # Questo file (italiano)
├── .gitignore                         # Esclusioni Python, TypeScript, Bash
├── .pre-commit-config.yaml            # Scansione segreti con gitleaks
├── docs/
│   └── presentations/                 # Materiali per talk/workshop in italiano
├── demo-specs/                        # Sviluppo guidato da spec (solo locale)
├── demo-hooks/                        # Automazione con hooks (solo locale)
├── demo-steering/                     # File di steering (solo locale)
├── demo-powers/                       # MCP Powers (solo locale)
├── demo-agents/                       # Workflow con agenti (deployabile)
└── showcase-serverless-assistant/     # Showcase end-to-end (deployabile)
```

---

## Licenza

Questo progetto è distribuito sotto la [Licenza MIT](LICENSE).
