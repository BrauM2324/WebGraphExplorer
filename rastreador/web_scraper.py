import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag, urlparse

INVALID_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".zip",
    ".mp4",
    ".mp3",
}


def is_valid(url: str) -> bool:
    if not url:
        return False

    url = url.strip()
    if url.startswith(("mailto:", "javascript:")):
        return False

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    if not parsed.netloc:
        return False

    path_lower = parsed.path.lower()
    if any(path_lower.endswith(ext) for ext in INVALID_EXTENSIONS):
        return False

    return True


def normalize_url(base_url: str, link: str) -> str:
    link = link.strip()
    if not link:
        return ""

    joined = urljoin(base_url, link)
    normalized, _ = urldefrag(joined)
    return normalized


def fetch_page(url: str) -> tuple[str, str, list[str]]:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return "", "", []

    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.title.string.strip() if soup.title and soup.title.string else ""
    content = soup.get_text(separator=" ", strip=True)

    links = []
    seen = set()
    for anchor in soup.find_all("a", href=True):
        raw_href = anchor["href"]
        normalized = normalize_url(url, raw_href)
        if normalized and normalized not in seen and is_valid(normalized):
            seen.add(normalized)
            links.append(normalized)

    return title_tag, content, links
