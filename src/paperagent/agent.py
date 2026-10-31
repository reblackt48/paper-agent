"""KI-Agent, der Fragen zu den gesammelten Papern beantwortet.

Start:  python -m paperagent.agent "Welche Paper erwähnen AlphaFold?"

Modell wählen über die Umgebungsvariable MODEL (siehe .env.example):
  - Claude per API:   MODEL=anthropic:claude-sonnet-5-5     (braucht ANTHROPIC_API_KEY)
  - Lokal, gratis:    MODEL=ollama:llama3.1                 (braucht installiertes Ollama)
"""
import os
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from paperagent import pipeline

load_dotenv()
DATA_PATH = os.getenv("DATA_PATH", "data/papers.csv")


# --- Tools: normale Python-Funktionen, die der Agent aufrufen darf ----------
# Der Docstring ist wichtig: Das LLM liest ihn, um zu entscheiden, WANN es das Tool nutzt.


@tool
def search_papers(keyword: str) -> str:
    """Sucht ein Stichwort in Titeln und Abstracts der gespeicherten Paper
    und gibt bis zu 5 Treffer mit Titel, Datum, URL und Abstract zurück."""
    df = pipeline.load(DATA_PATH)
    hits = pipeline.search_abstracts(df, keyword, top_n=5)
    if hits.empty:
        return f"Keine Treffer für '{keyword}'."
    return "\n\n".join(
        f"{r.title} ({r.published:%Y-%m-%d})\n{r.url}\n{r.abstract[:600]}"
        for r in hits.itertuples()
    )


@tool
def count_papers_per_year() -> str:
    """Gibt zurück, wie viele gespeicherte Paper pro Jahr veröffentlicht wurden."""
    df = pipeline.load(DATA_PATH)
    return df["published"].dt.year.value_counts().sort_index().to_string()


@tool
def refresh_data(query: str) -> str:
    """Lädt neue Paper zu einem Suchbegriff von arXiv und ersetzt die gespeicherten Daten."""
    df = pipeline.run_pipeline(query, path=DATA_PATH)
    return f"{len(df)} Paper zu '{query}' geladen."


SYSTEM_PROMPT = (
    "Du bist ein Assistent für wissenschaftliche Literatur. "
    "Nutze die Tools, um Fragen zu beantworten, und erfinde nichts. "
    "Nenne bei Aussagen über Paper immer den Titel. Antworte auf Deutsch."
)


def build_agent():
    model = init_chat_model(os.getenv("MODEL", "anthropic:claude-sonnet-5-5"))
    return create_agent(
        model,
        tools=[search_papers, count_papers_per_year, refresh_data],
        system_prompt=SYSTEM_PROMPT,
    )


def ask(agent, question: str) -> str:
    """Eine Frage stellen und die finale Textantwort zurückgeben."""
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    content = result["messages"][-1].content
    if isinstance(content, list):  # manche Modelle liefern Textblöcke
        content = "".join(b.get("text", "") for b in content if isinstance(b, dict))
    return content


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Wie viele Paper pro Jahr sind gespeichert?"
    print(ask(build_agent(), question))
