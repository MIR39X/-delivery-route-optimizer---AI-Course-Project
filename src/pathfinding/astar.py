import heapq
import math
import time


def heuristic(a, b, kind="manhattan"):
    if kind == "euclidean":
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def make_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def astar(grid, start, goal, heuristic_type="manhattan"):
    start_time = time.perf_counter()
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal, heuristic_type), 0, start))
    came_from = {}
    g_score = {start: 0}
    visited = []
    closed = set()
    count = 0

    while open_list:
        current = heapq.heappop(open_list)[2]

        if current in closed:
            continue

        closed.add(current)
        visited.append(current)

        if current == goal:
            path = make_path(came_from, current)
            end_time = time.perf_counter()
            return {
                "path": path,
                "visited": visited,
                "cost": g_score[current],
                "time": end_time - start_time,
                "found": True,
            }

        for neighbor in grid.neighbors(current):
            new_cost = g_score[current] + grid.cost(neighbor)
            if neighbor not in g_score or new_cost < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = new_cost
                count += 1
                f_score = new_cost + heuristic(neighbor, goal, heuristic_type)
                heapq.heappush(open_list, (f_score, count, neighbor))

    end_time = time.perf_counter()
    return {
        "path": [],
        "visited": visited,
        "cost": 0,
        "time": end_time - start_time,
        "found": False,
    }


def pair_key(a, b):
    return (a, b)


def build_pairs(grid, points, heuristic_type):
    pairs = {}
    for a in points:
        for b in points:
            if a != b:
                pairs[pair_key(a, b)] = astar(grid, a, b, heuristic_type)
    return pairs


def route_cost(order, pairs):
    total = 0
    for i in range(len(order) - 1):
        result = pairs.get(pair_key(order[i], order[i + 1]))
        if not result or not result["found"]:
            return None
        total += result["cost"]
    return total


def nearest_order(start, deliveries, pairs):
    order = [start]
    remaining = list(deliveries)
    current = start

    while remaining:
        best = None
        best_cost = None
        for point in remaining:
            result = pairs.get(pair_key(current, point))
            if result and result["found"]:
                if best is None or result["cost"] < best_cost:
                    best = point
                    best_cost = result["cost"]
        if best is None:
            return None
        order.append(best)
        remaining.remove(best)
        current = best

    return order


def improve_order(order, pairs):
    best = list(order)
    best_cost = route_cost(best, pairs)
    improved = True
    rounds = 0

    while improved and rounds < 20:
        improved = False
        rounds += 1
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best)):
                if j - i == 1:
                    continue
                test = best[:i] + best[i:j][::-1] + best[j:]
                cost = route_cost(test, pairs)
                if cost is not None and cost < best_cost:
                    best = test
                    best_cost = cost
                    improved = True

    return best, best_cost


def build_full_result(order, pairs):
    full_path = []
    all_visited = []
    total_cost = 0

    for i in range(len(order) - 1):
        result = pairs[pair_key(order[i], order[i + 1])]
        route_part = result["path"]
        if full_path and route_part:
            route_part = route_part[1:]
        full_path.extend(route_part)
        all_visited.extend(result["visited"])
        total_cost += result["cost"]

    return full_path, all_visited, total_cost


def multi_route(grid, heuristic_type="manhattan"):
    if not grid.start or not grid.deliveries:
        return {
            "path": [],
            "visited": [],
            "cost": 0,
            "time": 0,
            "found": False,
            "order": [],
            "nearest_cost": 0,
            "saved_cost": 0,
            "heuristic": heuristic_type,
            "message": "Add a start point and at least one delivery point.",
        }

    start_time = time.perf_counter()
    points = [grid.start] + list(grid.deliveries)
    pairs = build_pairs(grid, points, heuristic_type)
    first_order = nearest_order(grid.start, grid.deliveries, pairs)

    if first_order is None:
        end_time = time.perf_counter()
        return {
            "path": [],
            "visited": [],
            "cost": 0,
            "time": end_time - start_time,
            "found": False,
            "order": [],
            "nearest_cost": 0,
            "saved_cost": 0,
            "heuristic": heuristic_type,
            "message": "Some delivery points cannot be reached.",
        }

    first_cost = route_cost(first_order, pairs)
    final_order, final_cost = improve_order(first_order, pairs)
    full_path, all_visited, total_cost = build_full_result(final_order, pairs)

    end_time = time.perf_counter()
    return {
        "path": full_path,
        "visited": all_visited,
        "cost": total_cost,
        "time": end_time - start_time,
        "found": True,
        "order": final_order[1:],
        "nearest_order": first_order[1:],
        "nearest_cost": first_cost,
        "saved_cost": first_cost - final_cost,
        "heuristic": heuristic_type,
        "message": "Route found.",
    }
