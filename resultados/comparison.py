from utilidades.metrics import Metrics


def print_comparison_table(results):
    rows = [Metrics(result).report() for _, result in results]

    header = ["Algoritmo", "Nodos visitados", "Profundidad", "Tiempo (s)", "Resultados"]
    print("\n" + " | ".join(header))
    print("-" * 80)

    for row in rows:
        print(
            f"{row['algorithm']} | {row['nodes_visited']} | {row['max_depth']} | "
            f"{row['time_elapsed']:.4f} | {row['results_count']}"
        )

    print("\nResultados por algoritmo:")
    for name, result in results:
        print(f"- {name}: {len(result.results)} paginas relevantes encontradas")
        if result.results:
            preview = result.results[:3]
            print(f"  Primeros resultados: {', '.join(preview)}")


def _format_winners(results, metric, lower_is_better=True, value_getter=None):
    values = []
    for name, result in results:
        value = value_getter(result) if value_getter else getattr(result, metric)
        values.append((name, value))

    best_value = min(value for _, value in values) if lower_is_better else max(value for _, value in values)
    winners = [name for name, value in values if value == best_value]

    if len(winners) == 1:
        return winners[0], best_value, False
    return ", ".join(winners), best_value, True


def build_conclusion(results):
    best_time, time_value, tied_time = _format_winners(results, "time_elapsed")
    best_nodes, nodes_value, tied_nodes = _format_winners(results, "nodes_visited")
    best_depth, depth_value, tied_depth = _format_winners(results, "max_depth")
    best_results, results_value, tied_results = _format_winners(
        results,
        "results",
        lower_is_better=False,
        value_getter=lambda result: len(result.results),
    )

    time_line = (
        f"-> Empataron como mas rapidos: {best_time} ({time_value:.4f} s)."
        if tied_time
        else f"-> El algoritmo mas rapido fue {best_time} ({time_value:.4f} s)."
    )
    nodes_line = (
        f"-> Empataron con menos nodos visitados: {best_nodes} ({nodes_value} nodos)."
        if tied_nodes
        else f"-> El que visito menos nodos fue {best_nodes} ({nodes_value} nodos)."
    )
    depth_line = (
        f"-> Empataron con menor profundidad alcanzada: {best_depth} (profundidad {depth_value})."
        if tied_depth
        else f"-> El que alcanzo menor profundidad fue {best_depth} (profundidad {depth_value})."
    )
    results_line = (
        f"-> Empataron con mas paginas relevantes: {best_results} ({results_value} resultados)."
        if tied_results
        else f"-> El que encontro mas paginas relevantes fue {best_results} ({results_value} resultados)."
    )

    return "\n".join(
        [
            time_line,
            nodes_line,
            depth_line,
            results_line,
             ]
    )
