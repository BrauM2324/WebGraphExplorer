from utils.metrics import Metrics


def print_comparison_table(results):
    rows = [Metrics(result).report() for _, result in results]

    header = ["Algoritmo", "Nodos visitados", "Profundidad", "Tiempo (s)", "Resultados"]
    print("\n" + " | ".join(header))
    print("-" * 80)

    for row in rows:
        print(
            f"{row['algorithm']} | {row['nodes_visited']} | {row['max_depth']} | {row['time_elapsed']:.4f} | {row['results_count']}"
        )

    print("\nResultados por algoritmo:")
    for name, result in results:
        print(f"- {name}: {len(result.results)} páginas relevantes encontradas")
        if result.results:
            preview = result.results[:3]
            print(f"  Primeros resultados: {', '.join(preview)}")


def build_conclusion(results):
    sorted_by_time = sorted(results, key=lambda pair: pair[1].time_elapsed)
    best_time = sorted_by_time[0][0]

    sorted_by_nodes = sorted(results, key=lambda pair: pair[1].nodes_visited)
    best_nodes = sorted_by_nodes[0][0]

    sorted_by_depth = sorted(results, key=lambda pair: pair[1].max_depth)
    best_depth = sorted_by_depth[0][0]

    conclusion = (
        f"El algoritmo más rápido fue {best_time}. "
        f"El que visitó menos nodos fue {best_nodes}. "
        f"El que alcanzó menor profundidad fue {best_depth}. "
    )
    conclusion += (
        "Los resultados se basan en el crawling dinámico de páginas reales, "
        "por lo que los tiempos y profundidades pueden variar según el sitio y la conexión."
    )
    return conclusion
