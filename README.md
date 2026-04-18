# PathMind 🚀

PathMind is an advanced, high-performance pathfinding visualizer built with a sleek **Neo-Brutalist** aesthetic. It provides a real-time visualization of how various search algorithms explore complex grids and find optimal paths, blending educational value with premium design.

![PathMind Banner](file:///C:/Users/parth/.gemini/antigravity/brain/c49a796a-1048-42dd-b026-6f248df9e900/pathmind_banner_1776520873609.png)

## ✨ Key Features

- **🏎️ Algorithm Comparator**: A dedicated racing view where you can watch 6 algorithms (BFS, DFS, A*, UCS, Greedy, Bi-BFS) compete side-by-side on identical mazes to compare speed, efficiency, and optimality.
- **🌍 Real-World Showcase**: An interactive, application-first view mapping search algorithms to their real-world counterparts (e.g., BFS for Social Networks, A* for GPS, DLS for Tic-Tac-Toe AI).
- **🏗️ Neo-Brutalist Design**: A high-contrast, premium interface featuring sharp edges, bold typography (Plus Jakarta Sans), and a curated color palette for a truly modern feel.
- **⚡ High-Speed Execution**: Backend-driven pathfinding logic implemented in Python for precision, bridged with smooth HTML5 Canvas animations.
- **🛠️ Interactive Sandbox**: Paint walls, drag start/end markers, adjust search limits, and watch the algorithms adapt in real-time.
- **🌙 Theme Support**: Seamless switching between high-contrast Light and Dark modes.

## 🧠 Search Algorithms

PathMind implements a wide array of search strategies, categorized by their approach:

### 🧩 Uninformed Search (Blind)
- **Breadth-First Search (BFS)**: Guaranteed to find the shortest path in unweighted grids.
- **Depth-First Search (DFS)**: Prioritizes depth over optimality; efficient in memory but rarely shortest.
- **Uniform Cost Search (UCS)**: Dijkstra's algorithm optimized for grid costs.
- **Depth-Limited Search (DLS)**: A controlled version of DFS with a hard depth cutoff.
- **Bidirectional BFS**: Meets in the middle for exponential performance gains in large spaces.

### 🎯 Informed Search (Heuristic-based)
- **A* Search**: The "Gold Standard"—uses Manhattan heuristics to find optimal paths with minimal exploration.
- **Greedy Best-First Search**: Focused entirely on the goal; blazing fast but can get trapped in local optima.
- **IDA* (Iterative Deepening A*)**: Explores paths with increasing cost limits, combining the optimality of A* with the memory efficiency of DFS.

## 🛠️ Technical Stack

- **Backend**: Python 3.x / Flask
- **Frontend**: Vanilla JavaScript (ES6+), HTML5 Canvas, CSS3 Custom Properties
- **Logic**: Modular pathfinding library in `src/` supporting weighted and unweighted grids.
- **Styling**: Neo-Brutalist framework using `Plus Jakarta Sans` & `Syne`.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Pathmind.git
   cd Pathmind
   ```

2. **Set up a Virtual Environment** (recommended):
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**:
   ```bash
   python app.py
   ```

5. **Explore**:
   Navigate to `http://127.0.0.1:5000` in your browser.

## 📁 Project Architecture

```text
Pathmind/
├── app.py              # Flask Application Entry Point
├── src/                # Core Algorithm Implementations (A*, BFS, etc.)
├── comparator_logic/   # Multi-grid maze generation and racing logic
├── static/             # Frontend assets (CSS, JS)
├── templates/          # HTML Templates (Sandbox, Showcase, Comparator)
└── requirements.txt    # Project dependencies
```

## 🤝 Special Thanks

A huge thank you to **[paratesai316](https://github.com/paratesai316)** for the co-development of key features, including:
- **Real Map Implementation**: Integration of geographical coordination and grid-to-map mapping.
- **Flight Search**: Development of specialized pathfinding logic for airline routing and global city discovery.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
Developed with ❤️ by [Parth](https://github.com/git-parth-ch) 🚀
