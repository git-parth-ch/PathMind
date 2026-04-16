const colors = {
    wall: '#b0aba0',
    path: '#f2efe8',
    visited: '#d97706',
    optimal: '#e8380d',
    finalPath: '#2563eb',
    start: '#1a7a4a',
    end: '#c0321a'
};

let mazeData = null;
let algorithms = [];
let animationFrames = [];
const visitedAnimations = [];
const pathAnimations = [];

const API_BASE = window.location.origin;

function cssVar(name) {
    return getComputedStyle(document.body).getPropertyValue(name).trim();
}

function syncColorsToTheme() {
    colors.wall = cssVar('--wall');
    colors.path = cssVar('--paper');
    colors.visited = '#0ea5e9';    // Sky Blue for grid exploration
    colors.optimal = cssVar('--accent');
    colors.finalPath = '#f59e0b';  // Vibrant Orange/Amber for the final winning solved route
    colors.start = cssVar('--go');
    colors.end = cssVar('--stop');
}

function easeOutBack(t) {
    const c1 = 1.70158;
    const c3 = c1 + 1;
    return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
}

function drawCellPop(ctx, c, r, color, elapsed, totalMs, peakScale) {
    const t = Math.min(1, elapsed / totalMs);
    const scale = 0.5 + (peakScale - 0.5) * easeOutBack(t);
    const size = Math.max(0.001, scale);
    const offset = (1 - size) / 2;
    ctx.fillStyle = color;
    ctx.fillRect(c + offset, r + offset, size, size);
}

async function fetchMaze() {
    const res = await fetch(`${API_BASE}/api/generate_compare`);
    mazeData = await res.json();
    return mazeData;
}

async function solveMaze() {
    const res = await fetch(`${API_BASE}/api/solve_compare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mazeData)
    });
    algorithms = await res.json();
    initUI();
}

function initUI() {
    const grid = document.getElementById('canvas-grid');
    grid.innerHTML = '';
    
    for(let f of animationFrames) {
        if (f) cancelAnimationFrame(f);
    }
    animationFrames = [];
    
    algorithms.forEach((algo, i) => {
        algo.status = 'Waiting';
        algo.stepIndex = 0;
        algo.visitedSet = new Set();
        visitedAnimations[i] = new Map();
        pathAnimations[i] = new Map();
        
        const card = document.createElement('div');
        card.className = 'algo-card';
        card.onclick = () => toggleAlgo(i);
        
        card.innerHTML = `
            <div class="algo-header-row">
                <div class="algo-title">${algo.name}</div>
                <button class="expand-btn" title="Enlarge" onclick="toggleFullscreen(event, ${i})">⛶</button>
            </div>
            <div class="algo-status">
                <span id="status-${i}" style="color: var(--ink-muted);">Waiting (Click to Play)</span>
                <span id="time-${i}">-- s</span>
            </div>
            <div class="canvas-wrapper">
                <canvas id="canvas-${i}"></canvas>
            </div>
        `;
        grid.appendChild(card);
        requestAnimationFrame(() => drawMazeOptimized(i));
    });
    updateLeaderboard();
}

function drawMazeOptimized(algoIndex) {
    const canvas = document.getElementById(`canvas-${algoIndex}`);
    if(!canvas) return;
    const ctx = canvas.getContext('2d');
    
    const { maze, cols, rows, start, end } = mazeData;
    
    // Set strictly to internal columns and rows for 1:1 crisp grid scaling
    if(canvas.width !== cols || canvas.height !== rows){
        canvas.width = cols;
        canvas.height = rows;
    }
    
    const algo = algorithms[algoIndex];
    
    ctx.fillStyle = colors.path;
    ctx.fillRect(0, 0, cols, rows);
    
    ctx.fillStyle = colors.wall;
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (maze[r][c] === 1) {
                ctx.fillRect(c, r, 1, 1);
            }
        }
    }
    
    const now = performance.now();
    ctx.fillStyle = colors.visited;
    algo.visitedSet.forEach(key => {
        const [c, r] = key.split(',').map(Number);
        const startAt = visitedAnimations[algoIndex].get(key);
        if (startAt) {
            const elapsed = now - startAt;
            if (elapsed < 200) {
                drawCellPop(ctx, c, r, colors.visited, elapsed, 200, 1.08);
            } else {
                ctx.fillRect(c, r, 1, 1);
                visitedAnimations[algoIndex].delete(key);
            }
        } else {
            ctx.fillRect(c, r, 1, 1);
        }
    });
    
    if (algo.status === 'Finished' && algo.path) {
        ctx.fillStyle = colors.finalPath;
        for (let i = 0; i < algo.path.length; i++) {
            const [c, r] = algo.path[i];
            ctx.fillRect(c, r, 1, 1);
        }
    }
    
    ctx.fillStyle = colors.start;
    ctx.fillRect(start[0], start[1], 1, 1);
    
    ctx.fillStyle = colors.end;
    ctx.fillRect(end[0], end[1], 1, 1);
}

function updateLeaderboard() {
    const list = document.getElementById('leaderboard-list');
    const exportBtn = document.getElementById('btn-export-csv');
    
    const finishedAlgos = algorithms.filter(a => a.status === 'Finished');
    if (finishedAlgos.length === 0) {
        list.innerHTML = `<div style="color:var(--text-secondary); text-align:center;">Results will appear here as algorithms finish.</div>`;
        if (exportBtn) exportBtn.style.display = 'none';
        return;
    }
    
    if (exportBtn) exportBtn.style.display = 'block';
    
    const sorted = [...finishedAlgos].sort((a,b) => a.time - b.time);
    const sortedBySteps = [...finishedAlgos.filter(a => a.path && a.path.length > 0)].sort((a,b) => a.path.length - b.path.length);
    const shortestLen = sortedBySteps.length > 0 ? sortedBySteps[0].path.length : -1;
    
    list.innerHTML = '';
    
    sorted.forEach((algo, i) => {
        const item = document.createElement('div');
        item.className = 'leaderboard-item';
        if (i === 0) item.classList.add('first-place');
        
        let pathLen = algo.path && algo.path.length > 0 ? algo.path.length : 'N/A';
        const isShortest = pathLen === shortestLen;
        if (isShortest) item.classList.add('shortest-route');
        
        item.innerHTML = `
            <div class="item-header">
                ${i+1}. ${algo.name} ${isShortest ? '<span style="color:#10b981">⭐ Shortest</span>' : ''}
            </div>
            <div class="item-stats">
                Time: <strong>${algo.time.toFixed(5)}s</strong> | Route: ${pathLen}
            </div>
        `;
        list.appendChild(item);
    });
}

function animateAlgo(algoIndex) {
    const algo = algorithms[algoIndex];
    if (algo.status !== 'Running') return;
    
    const slider = document.getElementById('speed-slider');
    const stepsPerFrame = slider ? parseInt(slider.value) : 10;
    let done = false;
    
    for (let i = 0; i < stepsPerFrame; i++) {
        if (algo.stepIndex >= algo.visited_sequence.length) {
            done = true;
            break;
        }
        const cell = algo.visited_sequence[algo.stepIndex];
        const key = `${cell[0]},${cell[1]}`;
        if (!algo.visitedSet.has(key)) {
            visitedAnimations[algoIndex].set(key, performance.now());
        }
        algo.visitedSet.add(key);
        algo.stepIndex++;
    }
    
    if (done) {
        algo.status = 'Finished';
        if (algo.path) {
            const now = performance.now();
            algo.path.forEach(([c, r], index) => {
                pathAnimations[algoIndex].set(`${c},${r}`, now + index * 6);
            });
        }
        const stNode = document.getElementById(`status-${algoIndex}`);
        stNode.innerText = 'Finished';
        stNode.style.color = 'var(--go)';
        
        document.getElementById(`time-${algoIndex}`).innerText = `${algo.time.toFixed(4)} s`;
        updateLeaderboard();
    }
    
    // Crucial fix: The canvas must draw AFTER status is 'Finished' to render the optimal path!
    drawMazeOptimized(algoIndex);
    
    if (!done) {
        animationFrames[algoIndex] = requestAnimationFrame(() => animateAlgo(algoIndex));
    }
}

function toggleAlgo(i) {
    const algo = algorithms[i];
    const stNode = document.getElementById(`status-${i}`);
    
    if (algo.status === 'Waiting' || algo.status === 'Paused') {
        algo.status = 'Running';
        stNode.innerText = 'Running... (Click to pause)';
        stNode.style.color = 'var(--trace)';
        animateAlgo(i);
    } else if (algo.status === 'Running') {
        algo.status = 'Paused';
        stNode.innerText = 'Paused (Click to resume)';
        stNode.style.color = 'var(--stop)';
    }
}

function toggleFullscreen(e, index) {
    if (e) e.stopPropagation();
    const card = document.getElementById(`canvas-${index}`).closest('.algo-card');
    card.classList.toggle('fullscreen');
    const isFull = card.classList.contains('fullscreen');
    const btn = card.querySelector('.expand-btn');
    btn.innerText = isFull ? '✖' : '⛶';
}

document.getElementById('btn-start-all').onclick = () => {
    algorithms.forEach((algo, i) => {
        if (algo.status === 'Waiting' || algo.status === 'Paused') {
            toggleAlgo(i);
        }
    });
};

document.getElementById('btn-stop-all').onclick = () => {
    algorithms.forEach((algo, i) => {
        if (algo.status === 'Running') {
            toggleAlgo(i);
        }
    });
};

document.getElementById('btn-new-maze').onclick = async () => {
    const btn = document.getElementById('btn-new-maze');
    btn.innerText = 'Generating (Heavy compute)...';
    btn.disabled = true;
    
    await fetchMaze();
    await solveMaze();
    
    btn.innerText = 'Generate New Maze';
    btn.disabled = false;
};

const exportBtnRef = document.getElementById('btn-export-csv');
if (exportBtnRef) {
    exportBtnRef.onclick = () => {
        let csv = "Rank,Algorithm,Time (s),Path Length,Nodes Explored\n";
        const finishedAlgos = algorithms.filter(a => a.status === 'Finished');
        const sorted = [...finishedAlgos].sort((a,b) => a.time - b.time);
        
        sorted.forEach((algo, i) => {
            let pathLen = algo.path && algo.path.length > 0 ? algo.path.length : 'N/A';
            csv += `${i+1},"${algo.name}",${algo.time.toFixed(5)},${pathLen},${algo.visited_sequence.length}\n`;
        });
        
        const blob = new Blob([csv], { type: 'text/csv' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'pathmind_comparison_results.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };
}

document.getElementById('btn-theme-toggle').onclick = () => {
    document.body.classList.toggle('dark');
    const currentTheme = document.body.classList.contains('dark') ? 'dark' : 'light';
    localStorage.setItem('mazeTheme', currentTheme);
    syncColorsToTheme();
    algorithms.forEach((_, i) => drawMazeOptimized(i));
};

window.onload = async () => {
    const savedTheme = localStorage.getItem('mazeTheme');
    if (savedTheme === 'dark') document.body.classList.add('dark');
    syncColorsToTheme();
    await fetchMaze();
    await solveMaze();
};
