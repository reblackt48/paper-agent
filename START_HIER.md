# START HIER: Dein 1-Woche-Plan

Ziel: In ca. 20-25 Stunden ein kleines Projekt bauen (Agent + Datenpipeline + Tests + Git), das du im Gespräch erklären kannst.
Das Projekt liegt fertig als Gerüst im Ordner `paper-agent/`. **Wichtig:** Lies und verstehe jede Datei, ändere Dinge ab, probiere aus. Du wirst zu deinem Code gefragt.

---

## 1. Programme installieren (ca. 45 Min, heute Abend oder morgen früh)

| Programm | Wozu | Download |
|---|---|---|
| **Python 3.11 oder 3.12** | Programmiersprache (Version 3.10+ reicht) | python.org/downloads (Windows: Haken bei "Add Python to PATH"!) |
| **VS Code** | Editor | code.visualstudio.com, dazu die Erweiterung "Python" installieren |
| **Git** | Versionsverwaltung | git-scm.com (Mac: im Terminal `git --version` tippen, es bietet die Installation an) |
| **GitHub-Account** | Projekt veröffentlichen | github.com (kostenlos) |
| **Ein LLM für den Agenten** | siehe unten, Option A oder B | |

**LLM-Option A: Claude per API** (einfachste Variante): Konto auf console.anthropic.com, 5 $ Guthaben aufladen (reicht für das ganze Projekt), API-Key erstellen.
**LLM-Option B: Ollama** (lokal, gratis): ollama.com installieren, dann im Terminal `ollama pull llama3.1`. Braucht einen halbwegs aktuellen Rechner (ca. 8 GB RAM frei). Kleine lokale Modelle sind bei Tool Calling allerdings oft unzuverlässiger.

Terminal öffnen: Mac = "Terminal", Windows = "PowerShell", oder in VS Code Menü Terminal > New Terminal.

## 2. Projekt aufsetzen (ca. 20 Min)

Entpacke den Ordner `paper-agent`, öffne ihn in VS Code (File > Open Folder) und gib im VS-Code-Terminal ein:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
pytest                             # sollte 5 grüne Tests zeigen
```

(Mac/Linux evtl. `python3` statt `python`.) Danach `.env.example` kopieren zu `.env` und Modell/API-Key eintragen.

Git initialisieren:

```bash
git init
git add .
git commit -m "Initial project structure"
```
Dann auf GitHub ein neues leeres Repo anlegen und den dort angezeigten Befehlen folgen (`git remote add origin ...`, `git push -u origin main`).

---

## 3. Tagesplan (je ca. 3-4 Stunden)

### Tag 1: Git + Struktur + pytest
- Git-Grundlagen: [Git Handbook von GitHub](https://docs.github.com/en/get-started/using-git/about-git) oder ein 30-Min-YouTube-Tutorial ("Git for beginners"). Üben: Branch anlegen (`git switch -c feature-x`), committen, mergen, Pull Request auf GitHub erstellen.
- Verstehe die Ordnerstruktur: `src/` Code, `tests/` Tests, `requirements.txt` Abhängigkeiten, `.gitignore` was nicht ins Repo soll.
- pytest: Lies `tests/test_pipeline.py`. **Aufgabe:** Schreibe 2 eigene Tests dazu (z. B. leerer DataFrame bei `clean`).

### Tag 2: Datenpipeline
- Lies `src/paperagent/pipeline.py` Zeile für Zeile. Drei Schritte: Extract (API) -> Transform (clean) -> Load (CSV). Das ist ETL.
- `python -m paperagent.pipeline "protein structure prediction"` ausführen, `data/papers.csv` ansehen.
- pandas-Grundlagen: [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html).
- **Aufgabe:** Eine neue Funktion schreiben (z. B. Paper pro Monat zählen) und testen.

### Tag 3: Erster Agent
- Zuerst Konzept: Suche "LangChain agents" in der offiziellen Doku (docs.langchain.com). Lies Quickstart und die Seite zu Tools.
- Lies `src/paperagent/agent.py`: `@tool` macht aus Funktionen Tools, `create_agent` baut die Agent-Schleife.
- `python -m paperagent.agent "Wie viele Paper pro Jahr sind gespeichert?"` ausprobieren.
- **Kernmuster merken:** Frage -> Modell entscheidet Tool -> Tool läuft -> Ergebnis zurück ans Modell -> Antwort (ggf. mehrere Runden).
- **Aufgabe:** Ein eigenes Tool ergänzen (z. B. "zeige das neueste Paper").

### Tag 4: Verbinden + LangGraph anschauen
- Experimentiere: Was passiert bei unklaren Fragen? Wann nutzt der Agent welches Tool? Verbessere `SYSTEM_PROMPT` und die Tool-Docstrings.
- LangGraph (Konzept, 1 Stunde): Agenten als Graph aus Zuständen und Knoten. Die LangGraph-Doku "Quickstart" überfliegen. `create_agent` nutzt es im Hintergrund.
- Ein Thema aus Life Sciences oder Ingenieurwesen wählen, das zum Unternehmen passt (z. B. "bioprocess optimization"), und Daten dazu laden.

### Tag 5: Evaluation + Aufräumen
- `eval/questions.json` mit 10-15 eigenen Fragen erweitern, `python eval/run_eval.py` laufen lassen.
- Ergebnisse in der README unter "Ergebnisse der Evaluation" notieren: Was klappt, was nicht, warum?
- Code aufräumen, commit, push. Das Repo ist jetzt dein Portfolio.

### Tag 6: Erklär-Wissen + Gespräch
Nur auf Erklär-Niveau, jeweils ca. 45 Min:
- **Hugging Face**: huggingface.co ansehen (Hub = Modelle/Datasets, `transformers` = Bibliothek). Ausprobieren: `pip install transformers torch`, dann
  ```python
  from transformers import pipeline
  print(pipeline("sentiment-analysis")("This project is great"))
  ```
- **PyTorch**: [Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html) überfliegen: Tensor, Autograd, Training-Loop (Daten -> Vorhersage -> Loss -> Gradienten -> Update).
- **Simulation/Optimierung**: In 2 Sätzen erklären können. Beispiel: Ein Prozess wird als Modell simuliert, Optimierung sucht die besten Parameter; KI kann teure Simulationen durch Surrogatmodelle ersetzen oder Agenten können Simulationen automatisch ansteuern und auswerten. Optional: `scipy.optimize.minimize` mit einer Beispielfunktion testen.
- Das Projekt laut erklären üben (siehe unten).

### Tag 7: Puffer
Nachholen, Unternehmen recherchieren (Produkte, Forschungsfelder, Blog), Fragen vorbereiten.

---

## 4. Typische Fragen im Gespräch (Antworten vorbereiten)

1. Was hast du gebaut und warum so? (Pipeline -> Tools -> Agent -> Evaluation)
2. Wie funktioniert ein Agent? (Schleife aus Denken, Tool-Aufruf, Beobachtung)
3. Was war schwierig / was ging schief? (z. B. Agent wählt falsches Tool -> Docstrings/Prompt verbessert)
4. Wie testest du Software, die mit einem LLM arbeitet? (Deterministische Teile mit pytest, Agent mit Evaluationsset)
5. Was würdest du als Nächstes verbessern? (Vektorsuche/RAG statt Stichwortsuche, bessere Evaluation, mehr Datenquellen)
6. Was weißt du über PyTorch/Hugging Face? (Erklär-Niveau, ehrlich sagen, was du nur überblickt hast)

## 5. Tipps
- Nutze Claude zum Erklären ("Erkläre mir diese Funktion Zeile für Zeile") und bei Fehlermeldungen, aber tippe Änderungen selbst.
- Bleibe ehrlich: "Ich bin Einsteiger, habe mir in einer Woche X gezielt erarbeitet" überzeugt mehr als Übertreibung.
- Hängst du länger als 20 Minuten an einem Fehler: Fehlermeldung kopieren, fragen, weitermachen.
