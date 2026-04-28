from src.utils.constants import EMPTY, START, DELIVERY, OBSTACLE, WEIGHT, VISITED, PATH


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [[EMPTY for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.deliveries = []
        self.road_cells = None

    def inside(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def get(self, pos):
        r, c = pos
        return self.cells[r][c]

    def set_cell(self, pos, value):
        if not self.inside(pos):
            return

        old = self.get(pos)
        if old == START:
            self.start = None
        if old == DELIVERY and pos in self.deliveries:
            self.deliveries.remove(pos)

        if value == START:
            if self.start:
                sr, sc = self.start
                self.cells[sr][sc] = EMPTY
            self.start = pos
        if value == DELIVERY and pos not in self.deliveries:
            self.deliveries.append(pos)

        r, c = pos
        self.cells[r][c] = value

    def set_road_cells(self, road_cells):
        self.road_cells = set(road_cells)

    def is_road(self, pos):
        if self.road_cells is None:
            return True
        return pos in self.road_cells

    def nearest_road(self, pos):
        if self.is_road(pos):
            return pos
        seen = {pos}
        queue = [pos]
        while queue:
            current = queue.pop(0)
            for next_pos in self.all_neighbors(current):
                if next_pos in seen:
                    continue
                if self.is_road(next_pos):
                    return next_pos
                seen.add(next_pos)
                queue.append(next_pos)
        return pos

    def toggle_obstacle(self, pos):
        if self.get(pos) == OBSTACLE:
            self.set_cell(pos, EMPTY)
        else:
            self.set_cell(pos, OBSTACLE)

    def toggle_weight(self, pos):
        if self.get(pos) == WEIGHT:
            self.set_cell(pos, EMPTY)
        else:
            self.set_cell(pos, WEIGHT)

    def erase(self, pos):
        self.set_cell(pos, EMPTY)

    def clear_path(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c] in (VISITED, PATH):
                    self.cells[r][c] = EMPTY

    def reset(self):
        self.cells = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = None
        self.deliveries = []

    def walkable(self, pos):
        return self.get(pos) != OBSTACLE and self.is_road(pos)

    def cost(self, pos):
        if self.get(pos) == WEIGHT:
            return 5
        return 1

    def neighbors(self, pos):
        return [p for p in self.all_neighbors(pos) if self.walkable(p)]

    def all_neighbors(self, pos):
        r, c = pos
        possible = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        return [p for p in possible if self.inside(p)]
