def heuristic(url: str, title: str, content: str, keyword: str) -> float:
    score = 0.0
    kw = keyword.lower()

    if kw in url.lower():
        score += 3
    if kw in title.lower():
        score += 5
    if kw in content.lower():
        score += 10

    return score
