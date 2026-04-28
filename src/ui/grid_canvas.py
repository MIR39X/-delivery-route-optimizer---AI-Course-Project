import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from src.utils.constants import COLORS, EMPTY, START, DELIVERY, OBSTACLE, WEIGHT, VISITED, PATH


class GridCanvas(tk.Canvas):
    def __init__(self, master, grid, cell_size, click_func):
        width = grid.cols * cell_size
        height = grid.rows * cell_size
        super().__init__(master, width=width, height=height, bg=COLORS["map"], highlightthickness=0)
        self.grid_data = grid
        self.cell_size = cell_size
        self.click_func = click_func
        self.route_items = []
        self.vehicle = None
        self.bg_image = None
        self.bg_photo = None
        self.prepare_map()
        self.bind("<Button-1>", self.clicked)
        self.bind("<B1-Motion>", self.clicked)
        self.draw()

    def prepare_map(self):
        path = Path("assets/maps/large-city-map.png")
        if not path.exists():
            return
        w = self.grid_data.cols * self.cell_size
        h = self.grid_data.rows * self.cell_size
        image = Image.open(path).convert("RGBA")
        image = image.resize((w, h), Image.Resampling.LANCZOS)
        self.bg_image = image
        self.bg_photo = ImageTk.PhotoImage(image)
        self.grid_data.set_road_cells(self.find_roads(image))

    def road_pixel(self, r, g, b):
        bright = (r + g + b) / 3
        spread = max(r, g, b) - min(r, g, b)
        neutral = spread < 28
        road_gray = 145 <= bright <= 238
        not_green = not (g > r + 8 and g > b + 8)
        not_roof = not (r > g + 18 and r > b + 18)
        return neutral and road_gray and not_green and not_roof

    def road_score(self, image, x1, y1, x2, y2):
        hits = 0
        total = 0
        for px in range(max(0, x1), min(image.width, x2), 2):
            for py in range(max(0, y1), min(image.height, y2), 2):
                r, g, b, a = image.getpixel((px, py))
                total += 1
                if self.road_pixel(r, g, b):
                    hits += 1
        if total == 0:
            return 0
        return hits / total

    def find_roads(self, image):
        roads = set()
        for row in range(self.grid_data.rows):
            for col in range(self.grid_data.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x = x1 + self.cell_size // 2
                y = y1 + self.cell_size // 2
                center = self.road_score(image, x - 3, y - 3, x + 4, y + 4)
                horizontal = self.road_score(image, x - self.cell_size * 2, y - 4, x + self.cell_size * 2, y + 5)
                vertical = self.road_score(image, x - 4, y - self.cell_size * 2, x + 5, y + self.cell_size * 2)
                if center >= 0.45 and (horizontal >= 0.52 or vertical >= 0.52):
                    roads.add((row, col))
        return roads

    def clicked(self, event):
        row = event.y // self.cell_size
        col = event.x // self.cell_size
        if self.grid_data.inside((row, col)):
            self.click_func((row, col))

    def center(self, pos):
        r, c = pos
        return c * self.cell_size + self.cell_size // 2, r * self.cell_size + self.cell_size // 2

    def box(self, pos, pad=3):
        r, c = pos
        x1 = c * self.cell_size + pad
        y1 = r * self.cell_size + pad
        x2 = (c + 1) * self.cell_size - pad
        y2 = (r + 1) * self.cell_size - pad
        return x1, y1, x2, y2

    def draw(self):
        self.delete("all")
        self.route_items = []
        self.vehicle = None
        self.draw_background()
        for r in range(self.grid_data.rows):
            for c in range(self.grid_data.cols):
                self.draw_cell((r, c))

    def draw_background(self):
        w = self.grid_data.cols * self.cell_size
        h = self.grid_data.rows * self.cell_size
        path = Path("assets/maps/large-city-map.png")
        if path.exists() and self.bg_photo:
            self.create_image(0, 0, image=self.bg_photo, anchor="nw")
        else:
            self.create_rectangle(0, 0, w, h, fill=COLORS["map"], outline="")

        self.create_rectangle(0, 0, w, h, outline="#dbeafe", width=2)

    def draw_cell(self, pos):
        value = self.grid_data.get(pos)
        if value == START:
            self.draw_pin(pos, COLORS[START], "S")
        elif value == DELIVERY:
            self.draw_pin(pos, COLORS[DELIVERY], "D")
        elif value == OBSTACLE:
            self.draw_building(pos)
        elif value == WEIGHT:
            self.draw_weight(pos)
        elif value == VISITED:
            self.draw_visited(pos)
        elif value == PATH:
            self.draw_path_dot(pos)

    def draw_pin(self, pos, color, text):
        x, y = self.center(pos)
        self.create_oval(x - 8, y - 12, x + 8, y + 4, fill=color, outline="white", width=2)
        self.create_polygon(x - 5, y + 1, x + 5, y + 1, x, y + 11, fill=color, outline="white")
        self.create_text(x, y - 4, text=text, fill="white", font=("Segoe UI", 7, "bold"))

    def draw_building(self, pos):
        x1, y1, x2, y2 = self.box(pos, 5)
        self.create_rectangle(x1 + 2, y1 + 2, x2 + 2, y2 + 2, fill="#a7b2c0", outline="")
        self.create_rectangle(x1, y1, x2, y2, fill=COLORS[OBSTACLE], outline="#253044")
        self.create_line(x1 + 4, y1 + 4, x2 - 4, y2 - 4, fill="#64748b", width=2)
        self.create_line(x1 + 4, y2 - 4, x2 - 4, y1 + 4, fill="#64748b", width=2)

    def draw_weight(self, pos):
        x, y = self.center(pos)
        self.create_oval(x - 6, y - 6, x + 6, y + 6, fill=COLORS[WEIGHT], outline="white", width=2)
        self.create_text(x, y, text="5", fill="#2f2200", font=("Segoe UI", 7, "bold"))

    def draw_visited(self, pos):
        x, y = self.center(pos)
        self.create_oval(x - 2, y - 2, x + 2, y + 2, fill="#d9efff", outline="#60a5fa", width=1)

    def draw_path_dot(self, pos):
        x, y = self.center(pos)
        self.create_oval(x - 2, y - 2, x + 2, y + 2, fill=COLORS[PATH], outline="", width=1)

    def paint_temp(self, pos, value):
        old = self.grid_data.get(pos)
        if old in (EMPTY, VISITED, PATH):
            r, c = pos
            self.grid_data.cells[r][c] = value
            self.draw_cell(pos)

    def start_route(self):
        for item in self.route_items:
            self.delete(item)
        self.route_items = []
        self.vehicle = None

    def draw_route_segment(self, a, b):
        x1, y1 = self.center(a)
        x2, y2 = self.center(b)
        shadow = self.create_line(x1, y1, x2, y2, fill=COLORS["route_shadow"], width=5, capstyle="round", joinstyle="round")
        line = self.create_line(x1, y1, x2, y2, fill="#0b84ff", width=3, capstyle="round", joinstyle="round")
        if self.vehicle is None:
            self.vehicle = self.create_oval(x2 - 4, y2 - 4, x2 + 4, y2 + 4, fill=COLORS["vehicle"], outline=COLORS[PATH], width=2)
            self.route_items.append(self.vehicle)
        else:
            self.coords(self.vehicle, x2 - 4, y2 - 4, x2 + 4, y2 + 4)
            self.tag_raise(self.vehicle)
        self.route_items.extend([shadow, line])
        return self.vehicle

    def repaint_path(self, path):
        for pos in path:
            old = self.grid_data.get(pos)
            if old not in (START, DELIVERY):
                r, c = pos
                self.grid_data.cells[r][c] = PATH
                self.draw_path_dot(pos)
