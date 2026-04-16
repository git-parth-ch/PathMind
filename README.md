# PathMind 🚀

PathMind is an advanced, high-performance pathfinding visualizer built with a sleek **Neo-Brutalist** aesthetic. It provides a real-time visualization of how various search algorithms explore complex grids and find optimal paths.

![PathMind Screenshot](https://via.placeholder.com/800x450/0f0e0d/f2efe8?text=PathMind+Visualizer)

## ✨ Features

- **Dynamic Visualization**: Watch algorithms breathe and expand across the grid with smooth micro-animations.
- **Algorithm Comparison**: A dedicated **Comparator** view that races 6 algorithms side-by-side to compare performance and path optimality.
- **Neo-Brutalist UI**: A high-contrast, premium design system with sharp edges and a curated color palette.
- **Theming**: Full support for both **Light** and **Dark** modes with instant switching.
- **Interactive Grids**: Place walls, move start/end points, and even enlarge specific algorithm views in the comparator mode.

## 🧠 Supported Algorithms

### Uninformed Search
- **Breadth-First Search (BFS)**: Guarantees the shortest path on unweighted grids.
- **Depth-First Search (DFS)**: explores paths deeply; not optimal but light on resources.
- **Uniform Cost Search (UCS)**: Dijkstra's algorithm for grids; optimal for weighted movement.
- **Depth-Limited Search (DLS)**: DFS with a hard depth cutoff.

### Informed Search
- **A* Search**: The industry standard! Uses heuristics to find the shortest path efficiently.
- **Greedy Best-First Search**: Focuses solely on the goal; fast but not always optimal.

## 🛠️ Tech Stack

- **Backend**: Python / Flask
- **Frontend**: Vanilla JavaScript, HTML5 Canvas, CSS3
- **Design**: Syne & Plus Jakarta Sans typography, Neo-Brutalist CSS variables

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pathmind.git
   cd pathmind
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000`.

## 📁 Project Structure

```text
Pathmind/
├── app.py              # Main Flask entry point
├── src/                # Core algorithm implementations
├── comparator_logic/   # Multi-grid racing logic
├── static/             # Assets (CSS, JS, Fonts)
├── templates/          # HTML Templates
└── vercel.json         # Deployment configuration
```

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
Created by [Parth](https://github.com/yourusername) 🚀
