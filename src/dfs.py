from .utils import get_neighbors, reconstruct

def dfs(grid, s, e):
    """Depth-First Search — Stack (LIFO). Not guaranteed optimal."""
    stack = [s]
    parent = {s: None}
    order = []
    seen = set()
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        order.append(list(u))
        if u == e:
            break
        for v in get_neighbors(grid, *u):
            if v not in parent:
                parent[v] = u
                stack.append(v)
    return order, reconstruct(parent, s, e)
