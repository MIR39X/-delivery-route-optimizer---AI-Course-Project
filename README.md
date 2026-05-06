# Delivery Route Optimizer

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI Search](https://img.shields.io/badge/AI-A*_Search-2E7D32?style=for-the-badge)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-1565C0?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Fully_Developed-2E7D32?style=for-the-badge)

> A GUI-based AI route planning system that uses A* search to visualize optimal delivery paths, obstacles, explored nodes, weighted roads, and route cost.

## Overview

Delivery Route Optimizer is a fully developed Artificial Intelligence course project focused on route planning and pathfinding. The system allows users to place a start point, multiple delivery destinations, obstacles, and weighted roads on a grid-based map.

The application runs A* search, visualizes explored nodes, highlights the final route, and compares a simple nearest-stop delivery route with a locally improved route.

## Completed Features

- Interactive desktop grid interface
- Start and multiple delivery node selection
- Obstacle placement
- Weighted or high-cost road support
- A* search pathfinding
- Manhattan and Euclidean heuristic options
- Step-by-step explored node visualization
- Final route highlighting
- Multi-delivery route planning
- Nearest-route comparison with local-search improvement
- Route statistics including cost, path length, visited nodes, runtime, and delivery order
- Demo map and random map generation
- Adjustable animation speed
- Modern CustomTkinter interface with generated map and icon assets
- Unit-tested pathfinding behavior

## AI Technique

The main algorithm used in this project is **A* Search**.

A* evaluates each possible node using:

```text
f(n) = g(n) + h(n)
```

Where:

- `g(n)` is the actual cost from the start node to the current node
- `h(n)` is the estimated cost from the current node to the goal
- `f(n)` is the total estimated route cost

For multiple delivery points, the app builds a route using repeated A* searches, then applies a lightweight local-search improvement to reduce total route cost.

## Tech Stack

| Area | Technology |
| --- | --- |
| Language | Python |
| GUI | CustomTkinter + Tkinter Canvas |
| Algorithm | A* Search |
| Heuristics | Manhattan, Euclidean |
| Data Model | Grid / Graph |
| Project Type | AI route planning and visualization |

## Project Structure

```text
delivery-route-optimizer/
|-- assets/
|   `-- icons/
|-- docs/
|   `-- screenshots/
|-- src/
|   |-- models/
|   |-- pathfinding/
|   |-- ui/
|   `-- utils/
|-- tests/
|-- main.py
|-- .gitignore
`-- README.md
```

## Folder Purpose

| Folder | Purpose |
| --- | --- |
| `src/pathfinding/` | A* algorithm, route reconstruction, and delivery route optimization |
| `src/models/` | Grid and route state helpers |
| `src/ui/` | Tkinter window, canvas, controls, and visualization |
| `src/utils/` | Shared constants |
| `assets/` | Icons and visual assets |
| `docs/` | Reports, screenshots, and documentation |
| `tests/` | Unit tests for algorithm and project logic |

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

## How to Test

```bash
python -m unittest discover -s tests
```

## Project Status

This project is fully developed for the CS 2005 Artificial Intelligence course submission. The main implementation, GUI, route visualization, generated assets, and algorithm tests are complete.

## Team

| Member | ID |
| --- | --- |
| Arsalan Mir | 23K2085 |
| Vishal Dodeja | 23K2013 |

## Course

**CS 2005: Artificial Intelligence**  
AI Course Project
