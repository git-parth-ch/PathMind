from collections import deque
from .utils import get_neighbors, reconstruct

def bfs(grid, s, e):
    """Breadth-First Search — Queue (FIFO). Optimal for unweighted graphs."""
    queue = deque([s])
    parent = {s: None}
    order = []
    while queue:
        u = queue.popleft()
        order.append(list(u))
        if u == e:
            break
        for v in get_neighbors(grid, *u):
            if v not in parent:
                parent[v] = u
                queue.append(v)
    return order, reconstruct(parent, s, e)
