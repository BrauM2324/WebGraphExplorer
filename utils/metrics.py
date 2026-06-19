from dataclasses import dataclass
from typing import List


@dataclass
class SearchResult:
    algorithm: str
    nodes_visited: int
    max_depth: int
    results: List[str]
    time_elapsed: float


class Metrics:
    def __init__(self, search_result: SearchResult):
        self.search_result = search_result

    def report(self) -> dict:
        return {
            "algorithm": self.search_result.algorithm,
            "nodes_visited": self.search_result.nodes_visited,
            "max_depth": self.search_result.max_depth,
            "time_elapsed": self.search_result.time_elapsed,
            "results_count": len(self.search_result.results),
        }
