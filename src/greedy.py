import heapq
from .utils import get_neighbors, reconstruct, manhattan

def greedy(grid, s, e):
    """Greedy Best-First — Priority Queue using h(n) only. Not optimal."""
    heap = [(manhattan(s, e), s)]
    parent = {s: None}
    order = []
    seen = set()
    while heap:
        _, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u)
        order.append(list(u))
        if u == e:
            break
        for v in get_neighbors(grid, *u):
            if v not in parent:
                parent[v] = u
                heapq.heappush(heap, (manhattan(v, e), v))
    return order, reconstruct(parent, s, e)
