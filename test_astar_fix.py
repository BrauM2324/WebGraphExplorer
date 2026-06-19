#!/usr/bin/env python3
"""Script de pruebas para validar la corrección del algoritmo A*."""

from search_algorithms.bfs import bfs_search
from search_algorithms.dfs import dfs_search
from search_algorithms.astar import astar_search

def test_astar():
    print("=" * 60)
    print("VALIDANDO LA CORRECCIÓN DE A*")
    print("=" * 60)
    
    url = "https://www.python.org"
    keyword = "python"
    
    test_cases = [
        (5, 1),
        (10, 1),
        (15, 2),
    ]
    
    for max_nodes, max_depth in test_cases:
        print(f"\nPrueba: max_nodos={max_nodes}, max_profundidad={max_depth}")
        print("-" * 60)
        
        bfs = bfs_search(url, keyword, max_nodes=max_nodes, max_depth=max_depth)
        dfs = dfs_search(url, keyword, max_nodes=max_nodes, max_depth=max_depth)
        astar = astar_search(url, keyword, max_nodes=max_nodes, max_depth=max_depth)
        
        print(f"BFS:  {bfs.nodes_visited:3d} nodos, profundidad {bfs.max_depth}, {len(bfs.results):3d} resultados")
        print(f"DFS:  {dfs.nodes_visited:3d} nodos, profundidad {dfs.max_depth}, {len(dfs.results):3d} resultados")
        print(f"A*:   {astar.nodes_visited:3d} nodos, profundidad {astar.max_depth}, {len(astar.results):3d} resultados")
        
        # Comprobaciones
        assert astar.nodes_visited > 1, "¡A* debe visitar más de 1 nodo!"
        assert astar.nodes_visited <= max_nodes, f"A* visitó {astar.nodes_visited} > max_nodos {max_nodes}"
        assert astar.max_depth >= 0, "A* debe tener una profundidad válida"
        
        print("✓ Todas las comprobaciones pasaron para este caso de prueba")
    
    print("\n" + "=" * 60)
    print("✓ TODAS LAS PRUEBAS APROBADAS - A* CORREGIDO")
    print("=" * 60)

if __name__ == "__main__":
    test_astar()
