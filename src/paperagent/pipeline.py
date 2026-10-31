"""Datenpipeline: arXiv-Paper laden -> bereinigen -> speichern -> durchsuchen.

Jeder Schritt ist eine eigene kleine Funktion. Das macht den Code testbar
(siehe tests/test_pipeline.py) - genau das wird in der Stellenanzeige verlangt.
"""
import os
import xml.etree.ElementTree as ET

import pandas as pd
import requests

ARXIV_URL = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom"}
COLUMNS = ["title", "abstract", "published", "url"]


def fetch_papers(query: str, max_results: int = 30) -> pd.DataFrame:
    """Schritt 1 (Extract): Paper von der arXiv-API holen."""
    response = requests.get(
        ARXIV_URL,
        params={"search_query": f"all:{query}", "max_results": max_results},
        timeout=30,
    )
    response.raise_for_status()
    return parse_arxiv_xml(response.text)


def parse_arxiv_xml(xml_text: str) -> pd.DataFrame:
    """Die API liefert XML (Atom-Format). Hier wird daraus eine Tabelle."""
    root = ET.fromstring(xml_text)
    rows = []
    for entry in root.findall("a:entry", NS):
        rows.append(
            {
                "title": entry.findtext("a:title", default="", namespaces=NS),
                "abstract": entry.findtext("a:summary", default="", namespaces=NS),
                "published": entry.findtext("a:published", default="", namespaces=NS),
                "url": entry.findtext("a:id", default="", namespaces=NS),
            }
        )
    return pd.DataFrame(rows, columns=COLUMNS)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Schritt 2 (Transform): Whitespace entfernen, Duplikate und leere Abstracts raus."""
    df = df.copy()
    for col in ["title", "abstract"]:
        df[col] = df[col].fillna("").str.replace(r"\s+", " ", regex=True).str.strip()
    df = df[df["abstract"] != ""]
    df = df.drop_duplicates(subset="url")
    df["published"] = pd.to_datetime(df["published"], errors="coerce")
    return df.reset_index(drop=True)


def save(df: pd.DataFrame, path: str) -> None:
    """Schritt 3 (Load): als CSV speichern."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    df.to_csv(path, index=False)


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["published"] = pd.to_datetime(df["published"], errors="coerce")
    return df


def search_abstracts(df: pd.DataFrame, keyword: str, top_n: int = 5) -> pd.DataFrame:
    """Einfache Stichwortsuche in Titel und Abstract (ohne Groß-/Kleinschreibung)."""
    mask = df["title"].str.contains(keyword, case=False, regex=False) | df[
        "abstract"
    ].str.contains(keyword, case=False, regex=False)
    return df[mask].head(top_n)


def run_pipeline(query: str, max_results: int = 30, path: str = "data/papers.csv") -> pd.DataFrame:
    """Gesamte Pipeline: laden -> bereinigen -> speichern."""
    df = clean(fetch_papers(query, max_results))
    save(df, path)
    return df


if __name__ == "__main__":
    import sys

    q = sys.argv[1] if len(sys.argv) > 1 else "protein structure prediction"
    result = run_pipeline(q)
    print(f"{len(result)} Paper gespeichert in data/papers.csv")
