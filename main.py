from algoritmos_busqueda.bfs import bfs_search
from algoritmos_busqueda.dfs import dfs_search
from algoritmos_busqueda.astar import astar_search
from resultados.comparison import print_comparison_table, build_conclusion


def prompt_user():
    base_url = input("Ingrese la URL inicial: ").strip()
    keyword = input("Ingrese la palabra clave: ").strip()
    if not base_url or not keyword:
        raise ValueError("La URL inicial y la palabra clave son obligatorias.")
    return base_url, keyword


def main():
    try:
        base_url, keyword = prompt_user()

        print("\nEjecutando busqueda BFS...")
        bfs_result = bfs_search(base_url, keyword, max_nodes=30, max_depth=3)

        print("\nEjecutando busqueda DFS...")
        dfs_result = dfs_search(base_url, keyword, max_nodes=30, max_depth=3)

        print("\nEjecutando busqueda A*...")
        astar_result = astar_search(base_url, keyword, max_nodes=30, max_depth=3)

        results = [
            ("BFS", bfs_result),
            ("DFS", dfs_result),
            ("A*", astar_result),
        ]

        print_comparison_table(results)
        conclusion = build_conclusion(results)
        print("\nConclusion:")
        print(conclusion)

    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
