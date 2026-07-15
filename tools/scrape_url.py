import requests
from bs4 import BeautifulSoup

def execute(arguments: dict) -> str:

    url = arguments.get("url", "").strip()

    if not url:
        return "scrape_url error: URL not provided"

    try:
        resp = requests.get(
            url,
            timeout=12,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
        )
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header",
                         "aside", "form", "button", "noscript", "iframe"]):
            tag.decompose()

        main = soup.find("main") or soup.find("article") or soup.find("body")
        text = main.get_text(separator=" ", strip=True) if main else soup.get_text(separator=" ", strip=True)
        import re
        text = re.sub(r'\s+', ' ', text).strip()

        return text[:2000] if text else "No content found on this page."

    except Exception as e:
        return f"scrape_url error: {e}"


if __name__ == "__main__":
    print(execute({"url": "https://www.bbc.com/news"}))
