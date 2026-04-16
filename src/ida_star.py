from .utils import get_neighbors, reconstruct

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def ida_star(grid, start, end):
    order = []
    bound = heuristic(start, end)
    path = [start]
    path_set = {start}
    
    def search(g, bound):
        node = path[-1]
        order.append(list(node))
        f = g + heuristic(node, end)
        
        if f > bound:
            return f, None
        if node == end:
            return -1, path
            
        min_bound = float('inf')
        for neighbor in get_neighbors(grid, *node):
            if neighbor not in path_set:
                path.append(neighbor)
                path_set.add(neighbor)
                cost = grid[neighbor[0]][neighbor[1]] if grid[neighbor[0]][neighbor[1]] > 1 else 1
                t, res = search(g + cost, bound)
                if t == -1:
                    return -1, res
                if t < min_bound:
                    min_bound = t
                path.pop()
                path_set.remove(neighbor)
                
        return min_bound, None

    while True:
        t, res = search(0, bound)
        if t == -1:
            return order, [list(p) for p in res]
        if t == float('inf'):
            return order, []
        bound = t

