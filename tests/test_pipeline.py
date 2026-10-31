import pandas as pd

from paperagent.pipeline import clean, parse_arxiv_xml, search_abstracts

SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/1111.1111v1</id>
    <published>2023-05-01T10:00:00Z</published>
    <title>Deep   Learning
      for Proteins</title>
    <summary>  We study AlphaFold-like models.  </summary>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2222.2222v1</id>
    <published>2024-02-10T10:00:00Z</published>
    <title>Optimization of Bioreactors</title>
    <summary>Process optimization with surrogate models.</summary>
  </entry>
</feed>"""


def make_df():
    return pd.DataFrame(
        {
            "title": ["  A  title ", "B", "B again", "C"],
            "abstract": ["Some   text", "More text", "More text", ""],
            "published": ["2023-01-01", "2024-01-01", "2024-01-01", "2022-01-01"],
            "url": ["u1", "u2", "u2", "u3"],
        }
    )


def test_parse_arxiv_xml_returns_all_entries():
    df = parse_arxiv_xml(SAMPLE_XML)
    assert len(df) == 2
    assert list(df.columns) == ["title", "abstract", "published", "url"]


def test_clean_normalizes_whitespace():
    df = clean(parse_arxiv_xml(SAMPLE_XML))
    assert df.loc[0, "title"] == "Deep Learning for Proteins"
    assert df.loc[0, "abstract"] == "We study AlphaFold-like models."


def test_clean_removes_duplicates_and_empty_abstracts():
    df = clean(make_df())
    # u2 kommt doppelt vor, u3 hat keinen Abstract -> 2 Zeilen bleiben
    assert list(df["url"]) == ["u1", "u2"]


def test_search_is_case_insensitive():
    df = clean(parse_arxiv_xml(SAMPLE_XML))
    hits = search_abstracts(df, "alphafold")
    assert len(hits) == 1
    assert "Proteins" in hits.iloc[0]["title"]


def test_search_no_match_returns_empty():
    df = clean(parse_arxiv_xml(SAMPLE_XML))
    assert search_abstracts(df, "quantum").empty
