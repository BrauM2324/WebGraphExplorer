from collections import deque
from crawler.web_scraper import fetch_page
from utils.metrics import SearchResult
from utils.time_tracker import TimeTracker


def dfs_search(start_url: str, keyword: str, max_nodes: int = 30, max_depth: int = 3) -> SearchResult:
    tracker = TimeTracker()
    tracker.start()

    stack = deque([(start_url, 0)])
    visited = {start_url}
    found = []
    found_set = set()
    nodes_visited = 0
    max_reached_depth = 0
    graph = {}

    while stack and nodes_visited < max_nodes:
        current_url, depth = stack.pop()

        if depth > max_reached_depth:
            max_reached_depth = depth

        title, content, links = fetch_page(current_url)
        nodes_visited += 1
        graph[current_url] = links

        if keyword.lower() in current_url.lower() or keyword.lower() in title.lower() or keyword.lower() in content.lower():
            if current_url not in found_set:
                found_set.add(current_url)
                found.append(current_url)

        if depth < max_depth:
            for neighbor in reversed(links):
                if neighbor not in visited and nodes_visited < max_nodes:
                    visited.add(neighbor)
                    stack.append((neighbor, depth + 1))

    return SearchResult(
        algorithm="DFS",
        nodes_visited=nodes_visited,
        max_depth=max_reached_depth,
        results=found,
        time_elapsed=tracker.end(),
    )
