import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

def _get_tavily_key() -> str:
    try:
        import streamlit as st
        return st.secrets.get("TAVILY_API_KEY") or os.getenv("TAVILY_API_KEY", "")
    except Exception:
        return os.getenv("TAVILY_API_KEY", "")

def execute(arguments: dict) -> str:
    """
    Web search tool using Tavily API.
    Arguments: {"query": "search query here"}
    """
    query = arguments.get("query", "").strip()

    if not query:
        return "web_search error: query not provided"

    try:
        tavily = TavilyClient(api_key=_get_tavily_key())

        results = tavily.search(
            query=query,
            max_results=8,                
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,    
        )

        out = []

        if results.get("answer"):
            out.append(f"AI SUMMARY:\n{results['answer']}\n")

        out.append(f"SEARCH RESULTS FOR: {query}\n{'='*60}")

        sources = []  
        for i, r in enumerate(results.get("results", []), 1):
            
            raw = r.get("raw_content", "") or ""
            content = raw[:1200] if raw else r.get("content", "")[:800]
            title = r.get("title", "No title")
            url = r.get("url", "")

            out.append(
                f"\n[{i}] {title}\n"
                f"URL: {url}\n"
                f"Content: {content}"
            )
            out.append("-" * 50)
            sources.append(f"{i}. {title} — {url}")

        if sources:
            out.append("\n" + "="*60)
            out.append("ALL SOURCES:")
            out.extend(sources)

        return "\n".join(out)

    except Exception as e:
        return f"web_search error: {e}"


if __name__ == "__main__":
    print(execute({"query": "latest AI news 2026"}))
