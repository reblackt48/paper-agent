"""Mini-Evaluation: Fragen an den Agenten stellen und prüfen, ob erwartete Stichwörter vorkommen.

Das ist bewusst simpel. Im Gespräch kannst du erwähnen, dass man das z. B. mit
LLM-as-a-Judge oder einem größeren Testset ausbauen würde.
Ausführen:  python eval/run_eval.py   (nachdem die Daten geladen wurden)
"""
import json
from pathlib import Path

from paperagent.agent import ask, build_agent

questions = json.loads((Path(__file__).parent / "questions.json").read_text(encoding="utf-8"))
agent = build_agent()
passed = 0

for item in questions:
    answer = ask(agent, item["question"])
    ok = all(k.lower() in answer.lower() for k in item["expected_keywords"])
    passed += ok
    print(f"[{'OK' if ok else 'FAIL'}] {item['question']}\n    -> {answer[:200]!r}\n")

print(f"Ergebnis: {passed}/{len(questions)} bestanden")
