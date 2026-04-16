import heapq
from .utils import get_neighbors, reconstruct, manhattan

def astar(grid, s, e):
    """A* Search — Priority Queue with f(n) = g(n) + h(n). Optimal."""
    heap = [(manhattan(s, e), 0, s)]
    g = {s: 0}
    parent = {s: None}
    order = []
    seen = set()
    while heap:
        _, cost, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u)
        order.append(list(u))
        if u == e:
            break
        for v in get_neighbors(grid, *u):
            step_cost = grid[v[0]][v[1]] if grid[v[0]][v[1]] > 1 else 1
            nc = cost + step_cost
            if v not in g or nc < g[v]:
                g[v] = nc
                parent[v] = u
                heapq.heappush(heap, (nc + manhattan(v, e), nc, v))
    return order, reconstruct(parent, s, e)
