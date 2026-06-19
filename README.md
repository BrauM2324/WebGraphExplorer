# 🌐 Sistema de búsqueda en grafo web

## 🧠 ¿Qué hace el proyecto?

Este proyecto implementa un sistema de búsqueda web basado en grafos que permite comparar tres algoritmos de búsqueda:

- BFS (Búsqueda en anchura)
- DFS (Búsqueda en profundidad)
- A* (búsqueda informada con heurística)

El sistema:

1. Toma una URL base y una palabra clave del usuario
2. Recorre páginas web como un grafo dinámico
3. Cada página web es un nodo
4. Cada enlace `<a href="">` es una arista dirigida
5. Evita ciclos y duplicados (no visita la misma URL dos veces)
6. Construye el grafo mientras navega
7. Evalúa relevancia usando una heurística (A*)

---

## 🔒 REGLAS OBLIGATORIAS DEL SISTEMA

- Nunca visitar la misma URL dos veces (`visited` set obligatorio)
- Normalizar URLs:
  - convertir relativas a absolutas
  - eliminar fragmentos (`#section`)
- Filtrar URLs inválidas:
  - `mailto:`
  - `javascript:`
  - archivos `.pdf`
  - enlaces vacíos o corruptos
- Limitar crecimiento del grafo (opcional `MAX_NODES` / `MAX_DEPTH`)

---

## 🌐 ESTRUCTURA DEL GRAFO

El grafo se representa como:

```python
graph = {
    url: [lista de enlaces salientes]
}
```

Cada algoritmo usa este grafo, pero lo construye dinámicamente mientras explora.

---

## 📁 ESTRUCTURA DEL PROYECTO

- `main.py` → punto de entrada (solo orquesta)
- `crawler/`
  - `web_scraper.py` → descarga HTML y extrae enlaces
  - `web_graph.py` → estructura del grafo dinámico
- `search_algorithms/`
  - `bfs.py` → búsqueda en anchura
  - `dfs.py` → búsqueda en profundidad
  - `astar.py` → búsqueda A*
- `utils/`
  - `heuristics.py` → función de relevancia
  - `metrics.py` → métricas de rendimiento
  - `time_tracker.py` → medición de tiempo
- `results/`
  - `comparison.py` → tabla comparativa

---

## 🔍 ALGORITMOS

### BFS
- Explora por niveles
- Usa una cola (`queue`)
- Garantiza encontrar rutas cortas

---

### DFS
- Explora en profundidad
- Usa una pila (stack)
- Puede ser más rápido o desviarse

---

### A*
- Usa una cola de prioridad basada en una heurística
- Ordena nodos por relevancia (menor `f = g + h` primero)

---

## ⭐ HEURÍSTICA (A*)

La función evalúa relevancia de una página:

```python
heuristic(url, title, content, keyword)
```

Puntuación:

- `keyword` en URL → +3
- `keyword` en título → +5
- `keyword` en contenido → +10
- penalización por profundidad (opcional)

Mayor puntuación = mayor prioridad

---

## 📊 MÉTRICAS OBLIGATORIAS

Para cada algoritmo se mide:

- nodos visitados
- profundidad máxima
- tiempo de ejecución
- resultados encontrados

---

## ⏱️ MEDICIÓN DE TIEMPO

Cada algoritmo usa un medidor de tiempo:

- `start_time`
- `end_time`
- `elapsed_time()`

---

## 📈 SALIDA FINAL

El programa muestra:

1. Tabla comparativa:

```
Algoritmo | Nodos | Profundidad | Tiempo (s)
```

2. Conclusión automática explicando:

- cuál fue más rápido
- cuál visitó menos nodos
- cuál encontró resultados más eficientes

---

## ⚙️ EJECUCIÓN

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecutar:

```bash
python main.py
```

3. Ingresar:

- URL inicial
- palabra clave (keyword)

---

## 🧪 EJEMPLO

URL:
`https://example.com`

Palabra clave:
`example`

---

## 🎯 OBJETIVO FINAL

Comparar `BFS`, `DFS` y `A*` en un entorno real de web crawling modelado como grafo dinámico, evaluando eficiencia en tiempo, exploración y relevancia de resultados.