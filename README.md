# Paper-Agent

Ein KI-Agent, der Fragen zu wissenschaftlichen Papern beantwortet.

- **Datenpipeline** (`src/paperagent/pipeline.py`): lädt Paper über die arXiv-API, bereinigt sie und speichert sie als CSV
- **Agent** (`src/paperagent/agent.py`): LangChain-Agent, der die Pipeline-Funktionen als Tools nutzt
- **Tests** (`tests/`): pytest-Tests für die Pipeline
- **Evaluation** (`eval/questions.json`, `eval/run_eval.py`): Testfragen mit erwarteten Stichwörtern

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
cp .env.example .env             # dann MODEL / API-Key eintragen
```

## Benutzung

```bash
python -m paperagent.pipeline "protein structure prediction"   # Daten laden
python -m paperagent.agent "Welche Paper erwähnen AlphaFold?"  # Agent fragen
pytest                                                         # Tests
python eval/run_eval.py                                        # Evaluation
```

## Ergebnisse der Evaluation

_(Nach Tag 5 hier eintragen: wie viele Fragen richtig, was hat nicht geklappt, was wäre der nächste Schritt?)_
