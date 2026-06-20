from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = Path(__file__).resolve().parent / "static"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from algoritmos_busqueda.astar import astar_search
from algoritmos_busqueda.bfs import bfs_search
from algoritmos_busqueda.dfs import dfs_search
from resultados.comparison import build_conclusion

MAX_NODOS_INTERNO = 80
MAX_PROFUNDIDAD_INTERNA = 6


def _result_to_dict(result):
    return {
        "algoritmo": result.algorithm,
        "nodos_visitados": result.nodes_visited,
        "profundidad": result.max_depth,
        "tiempo": result.time_elapsed,
        "resultados": result.results,
        "grafo": result.graph or {},
        "recorrido": result.traversal or [],
    }


def _merge_graph(results):
    merged = {}
    for result in results:
        for url, links in (result.graph or {}).items():
            merged.setdefault(url, [])
            for link in links:
                if link not in merged[url]:
                    merged[url].append(link)
    return merged


def run_search(base_url, keyword, max_nodes=MAX_NODOS_INTERNO, max_depth=MAX_PROFUNDIDAD_INTERNA):
    bfs_result = bfs_search(base_url, keyword, max_nodes=max_nodes, max_depth=max_depth)
    dfs_result = dfs_search(base_url, keyword, max_nodes=max_nodes, max_depth=max_depth)
    astar_result = astar_search(base_url, keyword, max_nodes=max_nodes, max_depth=max_depth)

    results = [
        ("BFS", bfs_result),
        ("DFS", dfs_result),
        ("A*", astar_result),
    ]

    return {
        "url_inicial": base_url,
        "palabra_clave": keyword,
        "grafo": _merge_graph([bfs_result, dfs_result, astar_result]),
        "algoritmos": [_result_to_dict(result) for _, result in results],
        "conclusion": build_conclusion(results),
    }


class VisualizadorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/buscar":
            self._send_json(404, {"error": "Ruta no encontrada."})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            base_url = payload.get("url_inicial", "").strip()
            keyword = payload.get("palabra_clave", "").strip()
            max_nodes = int(payload.get("max_nodos", MAX_NODOS_INTERNO))
            max_depth = int(payload.get("max_profundidad", MAX_PROFUNDIDAD_INTERNA))

            if not base_url or not keyword:
                self._send_json(400, {"error": "La URL inicial y la palabra clave son obligatorias."})
                return

            self._send_json(200, run_search(base_url, keyword, max_nodes=max_nodes, max_depth=max_depth))
        except Exception as exc:
            self._send_json(500, {"error": f"No se pudo completar la busqueda: {exc}"})


def main():
    host = "127.0.0.1"
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer((host, port), VisualizadorHandler)
    print(f"Visualizador iniciado en http://{host}:{port}")
    print("Presione Ctrl+C para detenerlo.")
    server.serve_forever()


if __name__ == "__main__":
    main()
