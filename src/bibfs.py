from collections import deque
from .utils import get_neighbors, reconstruct

def bibfs(grid, s, e):
    """Bidirectional Breadth-First Search — Searches from start and end simultaneously."""
    if s == e: return [list(s)], [list(s)]
    
    q_f = deque([s])
    q_b = deque([e])
    
    parent_f = {s: None}
    parent_b = {e: None}
    
    order = []
    seen_f = {s}
    seen_b = {e}
    
    meet_node = None
    
    while q_f and q_b:
        u = q_f.popleft()
        order.append(list(u))
        if u in seen_b:
            meet_node = u
            break
        for v in get_neighbors(grid, *u):
            if v not in seen_f:
                seen_f.add(v)
                parent_f[v] = u
                q_f.append(v)
                if v in seen_b:
                    meet_node = v
                    break
                    
        if meet_node: break
        
        u_b = q_b.popleft()
        order.append(list(u_b))
        if u_b in seen_f:
            meet_node = u_b
            break
        for v in get_neighbors(grid, *u_b):
            if v not in seen_b:
                seen_b.add(v)
                parent_b[v] = u_b
                q_b.append(v)
                if v in seen_f:
                    meet_node = v
                    break
                    
        if meet_node: break

    if meet_node is None:
        return order, []
        
    path_f = reconstruct(parent_f, s, meet_node)
    path_b = reconstruct(parent_b, e, meet_node)
    
    path_b.reverse()
    if len(path_b) > 1:
        path = path_f + path_b[1:]
    else:
        path = path_f
        
    return order, path
