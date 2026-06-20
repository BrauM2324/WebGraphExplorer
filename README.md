# Sistema de busqueda en grafo web

## Que hace el proyecto

Este proyecto implementa un sistema de busqueda web basado en grafos para comparar tres algoritmos:

- BFS, busqueda en anchura
- DFS, busqueda en profundidad
- A*, busqueda informada con heuristica

El sistema toma una URL inicial y una palabra clave, recorre paginas web como un grafo dinamico y mide el comportamiento de cada algoritmo.

## Modelo del grafo

- Cada pagina web es un nodo.
- Cada enlace encontrado en una etiqueta `<a href="">` es una arista dirigida.
- El grafo se construye mientras el programa navega.
- Las URL visitadas se guardan para evitar ciclos y duplicados.
- Las URL relativas se convierten a absolutas.
- Los fragmentos como `#seccion` se eliminan.
- Se filtran enlaces invalidos como `mailto:`, `javascript:` y archivos no navegables.

La estructura interna del grafo es:

```python
grafo = {
    "url": ["lista de enlaces salientes"]
}
```

## Estructura del proyecto

- `main.py`: entrada por consola.
- `rastreador/web_scraper.py`: descarga paginas y extrae enlaces.
- `algoritmos_busqueda/bfs.py`: busqueda en anchura.
- `algoritmos_busqueda/dfs.py`: busqueda en profundidad.
- `algoritmos_busqueda/astar.py`: busqueda A*.
- `utilidades/heuristics.py`: calculo de relevancia.
- `utilidades/metrics.py`: datos y metricas de cada busqueda.
- `utilidades/time_tracker.py`: medicion de tiempo.
- `resultados/comparison.py`: tabla comparativa y conclusion.
- `visualizador/servidor.py`: servidor local de la interfaz visual.
- `visualizador/static/`: pantalla moderna con grafo animado.

## Metricas

Para cada algoritmo se registra:

- nodos visitados
- profundidad maxima alcanzada
- tiempo de ejecucion
- paginas relevantes encontradas
- grafo construido
- recorrido nodo por nodo

## Ejecucion por consola

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar:

```bash
python main.py
```

El programa pedira:

- URL inicial
- palabra clave

## Interfaz visual

Ejecutar:

```bash
python visualizador/servidor.py
```

Abrir en el navegador:

```text
http://127.0.0.1:8000
```

La interfaz muestra:

- fondo negro moderno
- grafo blanco con la URL inicial al centro
- recorrido animado de BFS, DFS y A*
- colores neon para cada algoritmo
- control para pausar, reanudar y repetir la animacion
- navegacion del grafo con zoom, arrastre del lienzo y arrastre de nodos
- tabla que se llena nodo por nodo
- comparacion final
- conclusion con manejo de empates

En la interfaz solo se ingresa:

- URL inicial
- palabra clave

## Heuristica de A*

La heuristica suma puntos cuando la palabra clave aparece en:

- URL: 3 puntos
- titulo: 5 puntos
- contenido: 10 puntos

Los nodos con mayor relevancia reciben mayor prioridad durante la busqueda A*.
