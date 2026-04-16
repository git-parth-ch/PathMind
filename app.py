from flask import Flask, render_template, request, jsonify
import time, sys
sys.setrecursionlimit(1000)

from src import bfs, dfs, ucs, dls, astar, greedy, bibfs

from comparator_logic.algorithm.bfs import solve as bfs_solve_compare
from comparator_logic.algorithm.dfs import solve as dfs_solve_compare
from comparator_logic.algorithm.a_star import solve as a_star_solve_compare
from comparator_logic.algorithm.dijkstra import solve as dijkstra_solve_compare
from comparator_logic.algorithm.best_first import solve as best_first_solve_compare
from comparator_logic.algorithm.uniform_cost import solve as ucs_solve_compare
from comparator_logic.algorithm.bibfs import solve as bibfs_solve_compare
from comparator_logic.maze.generator import generate_maze

app = Flask(__name__)

MAZE_COLS = 61
MAZE_ROWS = 61

def get_algorithm_data(name, generator_func, maze, start, end):
    visited_seq = []
    final_path = []
    start_time = time.perf_counter()
    for current, _, path in generator_func(maze, start, end):
        if current is not None:
            visited_seq.append(list(current)) # Ensure it's JSON serializable
        if path is not None and len(path) > 0:
            final_path = [list(p) for p in path]
            break
    exec_time = time.perf_counter() - start_time
    return {
        "name": name,
        "visited_sequence": visited_seq,
        "path": final_path,
        "time": exec_time
    }

ALGOS = {
    'bfs': bfs,
    'dfs': dfs,
    'ucs': ucs,
    'astar': astar,
    'greedy': greedy,
    'bibfs': bibfs,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comparator')
def comparator():
    return render_template('comparator.html')

@app.route("/api/generate_compare", methods=["GET"])
def generate_compare():
    maze = generate_maze(MAZE_COLS, MAZE_ROWS)
    start = (1, 1)
    end = (MAZE_COLS - 2, MAZE_ROWS - 2)
    return jsonify({
        "maze": maze,
        "start": start,
        "end": end,
        "cols": MAZE_COLS,
        "rows": MAZE_ROWS
    })

@app.route("/api/solve_compare", methods=["POST"])
def solve_compare():
    data = request.json
    maze = data["maze"]
    start = tuple(data["start"])
    end = tuple(data["end"])
    results = [
        get_algorithm_data("Breadth-First", bfs_solve_compare, maze, start, end),
        get_algorithm_data("Depth-First", dfs_solve_compare, maze, start, end),
        get_algorithm_data("A* Search", a_star_solve_compare, maze, start, end),
        get_algorithm_data("Uniform Cost", ucs_solve_compare, maze, start, end),
        get_algorithm_data("Greedy Best-First", best_first_solve_compare, maze, start, end),
        get_algorithm_data("Bidirectional BFS", bibfs_solve_compare, maze, start, end)
    ]
    return jsonify(results)

@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.json
    grid   = data['grid']
    start  = tuple(data['start'])
    end    = tuple(data['end'])
    algo   = data['algorithm']
    limit  = int(data.get('limit', 25))

    t0 = time.perf_counter()

    try:
        if algo == 'dls':
            visited, path = dls(grid, start, end, limit)
        elif algo in ALGOS:
            visited, path = ALGOS[algo](grid, start, end)
        else:
            return jsonify({'error': f'Unknown algorithm: {algo}'}), 400
    except RecursionError:
        return jsonify({'error': 'Recursion limit hit — reduce depth limit'}), 400

    elapsed_ms = (time.perf_counter() - t0) * 1000

    return jsonify({
        'visited': visited,
        'path': path,
        'stats': {
            'nodesExplored': len(visited),
            'pathLength':    len(path) - 1 if path else 0,
            'timeMs':        round(elapsed_ms, 3),
            'found':         len(path) > 0,
            'optimal':       algo in ('bfs', 'ucs', 'astar'),
        }
    })

if __name__ == '__main__':
    app.run(debug=False, port=5000)