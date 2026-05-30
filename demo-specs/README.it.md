# Demo: Sviluppo Guidato dalle Specifiche

> **Modalità di esecuzione:** solo locale — non richiede account AWS né connessione di rete

Questa demo mostra il workflow di sviluppo guidato dalle specifiche di Kiro, dove si definiscono i **requisiti**, si crea un **design**, lo si suddivide in **task**, e Kiro genera il codice di implementazione. Il risultato è un tool CLI per accorciare URL completamente tracciabile, costruito interamente a partire dagli artefatti delle specifiche.

## Il Workflow delle Specifiche

Il workflow delle specifiche di Kiro segue una pipeline strutturata:

```
requirements.md → design.md → tasks.md → codice sorgente generato
```

### 1. Requisiti (Requirements)

Definiscono **cosa** il sistema deve fare, usando user story e criteri di accettazione.

📄 `.kiro/specs/url-shortener/requirements.md`

I requisiti dell'URL shortener coprono:
- Validazione URL (schemi http/https, domini validi)
- Generazione short code (troncamento hash SHA-256, deterministico)
- Storage in memoria (basato su dizionario, solo per sessione)
- Interfaccia CLI (comandi shorten, resolve, list)

### 2. Design

Descrive **come** il sistema sarà costruito — modelli dati, interfacce, algoritmi.

📄 `.kiro/specs/url-shortener/design.md`

### 3. Task

Suddividono il design in **unità implementabili** con criteri di accettazione chiari.

📄 `.kiro/specs/url-shortener/tasks.md`

Ogni task è numerato (es. Task 1.1, Task 1.2) e mappa direttamente uno o più requisiti.

### 4. Codice Generato

Kiro genera codice sorgente che referenzia il task di origine nei commenti:

```python
# Task 1.1: Implement URL validation
def validate_url(url: str) -> tuple[bool, str | None]:
    ...

# Task 1.2: Implement short code generation
def generate_short_code(url: str) -> str:
    ...

# Task 1.3: Implement in-memory storage
class URLStore:
    ...

# Task 1.4: Implement CLI interface
def create_parser() -> argparse.ArgumentParser:
    ...
```

## Tracciabilità: Dalla Specifica al Sorgente

Ogni funzione in `src/url_shortener.py` porta un commento che la collega al task che l'ha generata. Questo crea una traccia di audit chiara:

| Task ID | Funzione / Classe | Requisito |
|---------|-------------------|-----------|
| Task 1.1 | `validate_url()` | Validazione URL |
| Task 1.2 | `generate_short_code()` | Generazione Short Code |
| Task 1.3 | `URLStore` | Storage in Memoria |
| Task 1.4 | `create_parser()`, `main()` | Interfaccia CLI |

## Struttura del Progetto

```
demo-specs/
├── .kiro/
│   └── specs/
│       └── url-shortener/
│           ├── .config.kiro
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
├── src/
│   └── url_shortener.py
├── tests/
│   └── test_url_shortener.py
├── requirements.txt
├── pyproject.toml
├── README.md
└── README.it.md
```

## Come Eseguire

```bash
# Installa le dipendenze
pip install -r requirements.txt

# Visualizza i comandi disponibili
python src/url_shortener.py --help

# Accorcia un URL
python src/url_shortener.py shorten https://example.com/long-path

# Risolvi uno short code
python src/url_shortener.py resolve abc123

# Elenca tutte le mappature
python src/url_shortener.py list
```

## Punti Chiave

- **Le specifiche sono documenti vivi** — evolvono con il progetto e servono come fonte di verità
- **I Task ID nel codice** creano tracciabilità tra decisioni di design e implementazione
- **Il workflow è ripetibile** — applicalo a qualsiasi progetto per uno sviluppo strutturato e assistito dall'AI
