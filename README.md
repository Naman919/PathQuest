# PathQuest — Pathfinding Algorithm Visualizer

PathQuest is an interactive visualization framework for studying and comparing graph search algorithms. Built in Python using Pygame, the project demonstrates how different pathfinding algorithms explore a grid environment and compute the shortest path while displaying real-time performance metrics.

This tool is designed for learning, experimentation, and algorithm analysis.

---

## Features

Interactive Grid Environment
Create barriers and design custom maps to test algorithms.

Multiple Pathfinding Algorithms

* Breadth-First Search (BFS)
* Depth-First Search (DFS)
* A* Search
* Dijkstra’s Algorithm
* Bidirectional A*
* Jump Point Search (JPS)

Maze Generation

* Structured recursive maze generation
* Random obstacle generation

Performance Metrics

For each algorithm execution PathQuest displays:

* Algorithm name
* Nodes explored
* Path length
* Execution time (milliseconds)

Interactive Controls

* Place start and end nodes
* Draw obstacles
* Reset path visualization
* Clear the grid
* Generate maze layouts

---

## Algorithms Implemented

| Algorithm         | Type                | Optimal                 | Notes                                       |
| ----------------- | ------------------- | ----------------------- | ------------------------------------------- |
| BFS               | Uninformed Search   | Yes (unweighted graphs) | Explores nodes level by level               |
| DFS               | Uninformed Search   | No                      | Explores deep paths first                   |
| Dijkstra          | Uniform Cost Search | Yes                     | Guarantees shortest path                    |
| A*                | Heuristic Search    | Yes                     | Uses heuristic to guide search              |
| Bidirectional A*  | Heuristic Search    | Yes                     | Searches from start and goal simultaneously |
| Jump Point Search | Optimized A*        | Yes                     | Reduces node expansions on uniform grids    |

---

## Installation

Clone the repository

```
git clone https://github.com/Naman919/PathQuest.git
```

Navigate into the project directory

```
cd PathQuest
```

Install dependencies

```
pip install -r requirements.txt
```

Run the program

```
python main.py
```

---

## Controls

Grid Interaction (Mouse)

* First click → Set Start Node
* Second click → Set End Node
* Additional clicks → Create Barriers

Control Panel (Right Side)

Algorithm Buttons

* BFS
* DFS
* A*
* Dijkstra
* Bidirectional
* JPS

Maze Options

* Maze: Structured
* Maze: Random

Utilities

* Reset Path Only
* Clear All

---

## Project Structure

```
PathQuest/
├── core/
│   ├── algorithms.py     
│   ├── engine.py        
│   └── heuristics.py    
├── ui/
│   ├── renderer.py      
│   └── components.py     
├── main.py               
├── requirements.txt
└── LICENSE
```

---

## Educational Purpose

PathQuest helps visualize how search algorithms behave in grid-based environments and how heuristics influence performance.

Concepts demonstrated include:

* Graph traversal
* Heuristic search
* Algorithm complexity
* Path reconstruction
* Maze generation

---

## Future Improvements

Potential enhancements:

* Diagonal movement support
* Weighted graphs
* Additional algorithms (Greedy Best-First, D* Lite)
* Benchmark mode for large-scale testing
* Visualization statistics dashboard
* Save / load grid configurations

---

This project is licensed under the MIT License.
