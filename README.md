# Delivery Route Optimizer

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI Search](https://img.shields.io/badge/AI-A*_Search-2E7D32?style=for-the-badge)
![GUI](https://img.shields.io/badge/GUI-Tkinter-1565C0?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In_Development-F9A825?style=for-the-badge)

> A GUI-based AI route planning system that uses A* search to visualize optimal delivery paths, obstacles, explored nodes, and route cost.

## Overview

Delivery Route Optimizer is an Artificial Intelligence course project focused on route planning and pathfinding. The system will allow users to place a start point, delivery destination, obstacles, and weighted roads on a grid-based map.

The application will then run the A* search algorithm, visualize the search process, and highlight the best route found.

## Planned Features

- Interactive desktop grid interface
- Start and destination node selection
- Obstacle placement
- Weighted or high-cost road support
- A* search pathfinding
- Step-by-step explored node visualization
- Final route highlighting
- Route statistics including cost, path length, and visited nodes

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

This makes A* suitable for efficient shortest-path search in grid-based maps and delivery route planning problems.

## Tech Stack

| Area | Technology |
| --- | --- |
| Language | Python |
| GUI | Tkinter |
| Algorithm | A* Search |
| Data Model | Grid / Graph |
| Project Type | AI route planning and visualization |

## Project Structure

```text
delivery-route-optimizer/
├── assets/
│   └── icons/
├── docs/
│   └── screenshots/
├── src/
│   ├── models/
│   ├── pathfinding/
│   ├── ui/
│   └── utils/
├── tests/
├── .gitignore
└── README.md
```

## Folder Purpose

| Folder | Purpose |
| --- | --- |
| `src/pathfinding/` | A* algorithm and route reconstruction logic |
| `src/models/` | Grid, cell, node, and route data structures |
| `src/ui/` | Tkinter windows, canvas, controls, and visualization |
| `src/utils/` | Shared constants and helper functions |
| `assets/` | Icons and visual assets |
| `docs/` | Reports, screenshots, and documentation |
| `tests/` | Unit tests for algorithm and project logic |

## Development Roadmap

1. Implement the A* pathfinding algorithm
2. Create grid and cell models
3. Build the Tkinter grid interface
4. Add obstacle and weighted-road editing
5. Animate explored nodes and final path
6. Display route statistics
7. Add screenshots and final report

## Team

| Member | ID |
| --- | --- |
| Arsalan Mir | 23K2085 |
| Vishal Dodeja | 23K2013 |

## Course

**CS 2005: Artificial Intelligence**  
AI Course Project

