from .utils import get_neighbors, reconstruct

def dls(grid, s, e, limit):
    """Depth-Limited Search — DFS with a hard depth cutoff."""
    parent = {s: None}
    order = []
    seen = set()

    def recurse(u, depth):
        if depth > limit:
            return False
        seen.add(u)
        order.append(list(u))
        if u == e:
            return True
        for v in get_neighbors(grid, *u):
            if v not in seen:
                parent[v] = u
                if recurse(v, depth + 1):
                    return True
        return False

    recurse(s, 0)
    return order, reconstruct(parent, s, e)
