from collections import deque
from .utils import get_neighbors, reconstruct_path

def solve(maze, start, end):
    if start == end:
        yield start, {start}, [start]
        return
        
    q_f = deque([start])
    q_b = deque([end])
    
    parent_f = {}
    parent_b = {}
    
    seen_f = {start}
    seen_b = {end}
    visited = set()
    
    meet_node = None
    
    while q_f and q_b:
        # Forward
        u = q_f.popleft()
        visited.add(u)
        
        if u in seen_b:
            meet_node = u
            break
            
        yield u, visited, None
        
        for v in get_neighbors(maze, u):
            if v not in seen_f:
                seen_f.add(v)
                parent_f[v] = u
                q_f.append(v)
                if v in seen_b:
                    meet_node = v
                    break
                    
        if meet_node: break
        
        # Backward
        u_b = q_b.popleft()
        visited.add(u_b)
        
        if u_b in seen_f:
            meet_node = u_b
            break
            
        yield u_b, visited, None
        
        for v in get_neighbors(maze, u_b):
            if v not in seen_b:
                seen_b.add(v)
                parent_b[v] = u_b
                q_b.append(v)
                if v in seen_f:
                    meet_node = v
                    break
                    
        if meet_node: break

    if meet_node is None:
        yield None, visited, []
        return
        
    path_f = reconstruct_path(parent_f, meet_node)
    path_f.reverse() # path_f is meet_node -> start, reverse to start -> meet_node
    
    path_b = reconstruct_path(parent_b, meet_node)
    # path_b is meet_node -> end. 
    
    if len(path_b) > 1:
        path = path_f + path_b[1:]
    else:
        path = path_f
        
    # include meet_node as the last visited yielding
    visited.add(meet_node)
    yield meet_node, visited, path
