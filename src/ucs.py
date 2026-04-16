import heapq
from .utils import get_neighbors, reconstruct

def ucs(grid, s, e):
    """Uniform Cost Search — Priority Queue (min-heap). Dijkstra on grid."""
    heap = [(0, s)]
    dist = {s: 0}
    parent = {s: None}
    order = []
    seen = set()
    while heap:
        cost, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u)
        order.append(list(u))
        if u == e:
            break
        for v in get_neighbors(grid, *u):
            step_cost = grid[v[0]][v[1]] if grid[v[0]][v[1]] > 1 else 1
            nc = cost + step_cost
            if v not in dist or nc < dist[v]:
                dist[v] = nc
                parent[v] = u
                heapq.heappush(heap, (nc, v))
    return order, reconstruct(parent, s, e)
