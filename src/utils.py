DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
            yield (nr, nc)

def reconstruct(parent, start, end):
    if end not in parent:
        return []
    path, cur = [], end
    while cur is not None:
        path.append(list(cur))
        cur = parent[cur]
    path.reverse()
    return path if path and path[0] == list(start) else []

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
