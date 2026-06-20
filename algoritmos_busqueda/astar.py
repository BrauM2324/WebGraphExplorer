import heapq
from rastreador.web_scraper import fetch_page
from utilidades.metrics import SearchResult
from utilidades.heuristics import heuristic
from utilidades.time_tracker import TimeTracker


def astar_search(start_url: str, keyword: str, max_nodes: int = 30, max_depth: int = 3) -> SearchResult:
    tracker = TimeTracker()
    tracker.start()

    visited = set()
    found = []
    found_set = set()
    nodes_visited = 0
    max_reached_depth = 0
    graph = {}
    traversal = []

    heap = []
    title, content = "", ""
    try:
        title, content, _ = fetch_page(start_url)
    except Exception:
        title, content = "", ""

    start_g = 0
    start_h = heuristic(start_url, title, content, keyword)
    start_f = start_g - start_h
    heapq.heappush(heap, (start_f, start_g, start_url))

    while heap and nodes_visited < max_nodes:
        _f_score, g_score, current_url = heapq.heappop(heap)

        if current_url in visited:
            continue

        visited.add(current_url)
        
        if g_score > max_reached_depth:
            max_reached_depth = g_score

        title, content, links = fetch_page(current_url)
        nodes_visited += 1
        graph[current_url] = links
        traversal.append(
            {
                "url": current_url,
                "depth": g_score,
                "order": nodes_visited,
                "title": title,
                "found": keyword.lower() in current_url.lower()
                or keyword.lower() in title.lower()
                or keyword.lower() in content.lower(),
                "score": heuristic(current_url, title, content, keyword),
            }
        )

        if traversal[-1]["found"]:
            if current_url not in found_set:
                found_set.add(current_url)
                found.append(current_url)

        if g_score < max_depth:
            for neighbor in links:
                if neighbor not in visited and nodes_visited < max_nodes:
                    neighbor_g = g_score + 1
                    neighbor_h = heuristic(neighbor, "", "", keyword)
                    neighbor_f = neighbor_g - neighbor_h
                    heapq.heappush(heap, (neighbor_f, neighbor_g, neighbor))

    return SearchResult(
        algorithm="A*",
        nodes_visited=nodes_visited,
        max_depth=max_reached_depth,
        results=found,
        time_elapsed=tracker.end(),
        graph=graph,
        traversal=traversal,
    )
