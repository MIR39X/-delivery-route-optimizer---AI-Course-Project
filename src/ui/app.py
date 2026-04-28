import random
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

import customtkinter as ctk
from PIL import Image

from src.models.grid import Grid
from src.pathfinding.astar import multi_route
from src.ui.grid_canvas import GridCanvas
from src.ui.sliding_selector import SlidingSelector
from src.utils.constants import ROWS, COLS, CELL_SIZE, EMPTY, START, DELIVERY, OBSTACLE, WEIGHT, VISITED, PATH, COLORS


class RouteApp(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        super().__init__()
        self.title("Delivery Route Optimizer")
        self.configure(fg_color="#eef4fb")
        self.resizable(True, True)
        self.grid_data = Grid(ROWS, COLS)
        self.mode = START
        self.running = False
        self.buttons = {}
        self.heuristic_choice = ctk.StringVar(value="manhattan")
        self.speed_choice = ctk.StringVar(value="Normal")
        self.status_text = ctk.StringVar(value="Place start and delivery points")
        self.cell_size = self.get_cell_size()
        self.icons = self.load_icons()
        self.make_ui()
        self.fit_window()

    def get_cell_size(self):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        by_width = (screen_w - 500) // COLS
        by_height = (screen_h - 180) // ROWS
        return max(10, min(CELL_SIZE, by_width, by_height))

    def fit_window(self):
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        win_w = min(self.winfo_reqwidth(), screen_w - 70)
        win_h = min(self.winfo_reqheight(), screen_h - 90)
        x = max(0, (screen_w - win_w) // 2)
        y = max(0, (screen_h - win_h) // 2)
        self.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.minsize(1000, 620)

    def make_ui(self):
        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=16, pady=14)

        header = ctk.CTkFrame(outer, fg_color="transparent")
        header.pack(fill="x", pady=(0, 12))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(left, text="Delivery Route Optimizer", font=("Segoe UI", 26, "bold"), text_color="#111827").pack(anchor="w")
        ctk.CTkLabel(left, text="A* route planning with live map exploration", font=("Segoe UI", 13), text_color="#64748b").pack(anchor="w")

        status = ctk.CTkLabel(header, textvariable=self.status_text, font=("Segoe UI", 12, "bold"), fg_color="#1a73e8", text_color="white", corner_radius=16, padx=16, pady=8)
        status.pack(side="right", pady=(10, 0))

        body = ctk.CTkFrame(outer, fg_color="transparent")
        body.pack(fill="both", expand=True)

        map_shell = ctk.CTkFrame(body, fg_color="white", corner_radius=18)
        map_shell.pack(side="left", fill="both", expand=True, padx=(0, 14))

        map_top = ctk.CTkFrame(map_shell, fg_color="transparent")
        map_top.pack(fill="x", padx=14, pady=(12, 8))
        ctk.CTkLabel(map_top, text="Live Route Map", font=("Segoe UI", 15, "bold"), text_color="#111827").pack(side="left")
        ctk.CTkLabel(map_top, text="Click or drag to edit cells", font=("Segoe UI", 11), text_color="#64748b").pack(side="right")

        canvas_box = ctk.CTkFrame(map_shell, fg_color="#f8fafc", corner_radius=14)
        canvas_box.pack(padx=12, pady=(0, 12))

        self.canvas = GridCanvas(canvas_box, self.grid_data, self.cell_size, self.cell_clicked)
        self.canvas.pack(padx=10, pady=10)

        side = ctk.CTkFrame(body, width=330, fg_color="#ffffff", corner_radius=18)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        self.make_sidebar(side)
        self.set_mode(START)
        self.update_stats()

    def load_icons(self):
        folder = Path("assets/icons/transparent")
        files = {
            "start": "Pin_Green.png",
            "delivery": "Pin_Red.png",
            "block": "RoadBlock.png",
            "weight": "Yellow_Some.png",
            "erase": "Eraser.png",
            "run": "TruckIcon.png",
            "clear": "BrushButton.png",
            "demo": "MapIcon.png",
            "random": "GridIcon.png",
            "reset": "GridPic.png",
            "route": "RouteIcon.png",
        }
        icons = {}
        for key, name in files.items():
            path = folder / name
            if path.exists():
                img = Image.open(path)
                icons[key] = ctk.CTkImage(light_image=img, dark_image=img, size=(22, 22))
        return icons

    def make_sidebar(self, side):
        content = ctk.CTkFrame(side, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=14, pady=14)

        self.make_mode_buttons(content)
        self.make_settings(content)
        self.make_action_buttons(content)
        self.make_legend(content)

        self.stats = ctk.CTkTextbox(content, height=190, fg_color="#f8fafc", text_color="#111827", border_color="#e2e8f0", border_width=1, corner_radius=12, font=("Consolas", 10))
        self.stats.pack(fill="x", pady=(8, 0))
        self.stats.configure(state="disabled")

    def section(self, master, title):
        box = ctk.CTkFrame(master, fg_color="#f8fafc", corner_radius=14)
        box.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(box, text=title, font=("Segoe UI", 14, "bold"), text_color="#111827").pack(anchor="w", padx=12, pady=(10, 6))
        inner = ctk.CTkFrame(box, fg_color="transparent")
        inner.pack(fill="x", padx=10, pady=(0, 10))
        return inner

    def icon_for_mode(self, value):
        names = {
            START: "start",
            DELIVERY: "delivery",
            OBSTACLE: "block",
            WEIGHT: "weight",
            EMPTY: "erase",
        }
        return self.icons.get(names.get(value))

    def make_mode_buttons(self, side):
        box = self.section(side, "Map Tools")
        modes = [
            (START, "Start"),
            (DELIVERY, "Delivery"),
            (OBSTACLE, "Block"),
            (WEIGHT, "Weight"),
            (EMPTY, "Erase"),
        ]
        for value, text in modes:
            btn = ctk.CTkButton(box, text=text, image=self.icon_for_mode(value), compound="left", height=34, corner_radius=10, fg_color="#ffffff", hover_color="#dbeafe", text_color="#111827", command=lambda v=value: self.set_mode(v))
            btn.pack(fill="x", pady=3)
            self.buttons[value] = btn

    def make_settings(self, side):
        box = self.section(side, "Routing")
        ctk.CTkLabel(box, text="Heuristic", font=("Segoe UI", 11), text_color="#64748b").pack(anchor="w")
        heuristic = SlidingSelector(box, ["manhattan", "euclidean"], self.heuristic_choice, lambda value: self.update_stats())
        heuristic.pack(fill="x", pady=(4, 10))

        ctk.CTkLabel(box, text="Animation", font=("Segoe UI", 11), text_color="#64748b").pack(anchor="w")
        speed = SlidingSelector(box, ["Fast", "Normal", "Slow"], self.speed_choice)
        speed.pack(fill="x", pady=(4, 0))

    def make_action_buttons(self, side):
        box = self.section(side, "Actions")
        ctk.CTkButton(box, text="Run Route", image=self.icons.get("run"), compound="left", height=38, corner_radius=12, fg_color="#1a73e8", hover_color="#1558bd", command=self.run_route).pack(fill="x", pady=(0, 7))
        actions = [
            ("Clear Path", self.clear_path, "clear"),
            ("Demo Map", self.demo_map, "demo"),
            ("Random Map", self.random_map, "random"),
            ("Reset Grid", self.reset_grid, "reset"),
        ]
        for text, command, icon in actions:
            ctk.CTkButton(box, text=text, image=self.icons.get(icon), compound="left", height=34, corner_radius=10, fg_color="#ffffff", hover_color="#e2e8f0", text_color="#111827", command=command).pack(fill="x", pady=3)

    def make_legend(self, side):
        box = self.section(side, "Legend")
        items = [
            ("start", COLORS[START], "Start"),
            ("delivery", COLORS[DELIVERY], "Delivery"),
            ("block", COLORS[OBSTACLE], "Blocked"),
            ("weight", COLORS[WEIGHT], "Cost 5"),
            ("route", COLORS[PATH], "Route"),
        ]
        for icon, color, text in items:
            row = ctk.CTkFrame(box, fg_color="transparent")
            row.pack(fill="x", pady=2)
            if self.icons.get(icon):
                ctk.CTkLabel(row, text="", image=self.icons[icon], width=22, height=22).pack(side="left")
            else:
                ctk.CTkLabel(row, text="", width=18, height=18, fg_color=color, corner_radius=5).pack(side="left")
            ctk.CTkLabel(row, text=text, font=("Segoe UI", 11), text_color="#64748b").pack(side="left", padx=8)

    def set_mode(self, mode):
        self.mode = mode
        for key, btn in self.buttons.items():
            if key == mode:
                btn.configure(fg_color="#dbeafe", text_color="#1a73e8")
            else:
                btn.configure(fg_color="#ffffff", text_color="#111827")
        names = {
            START: "Start",
            DELIVERY: "Delivery",
            OBSTACLE: "Block",
            WEIGHT: "Weight",
            EMPTY: "Erase",
        }
        self.status_text.set(f"Tool: {names[mode]}")

    def get_delay(self):
        values = {"Fast": 3, "Normal": 8, "Slow": 18}
        return values.get(self.speed_choice.get(), 8)

    def cell_clicked(self, pos):
        if self.running:
            return
        self.grid_data.clear_path()
        if self.mode == START:
            pos = self.grid_data.nearest_road(pos)
            self.grid_data.set_cell(pos, START)
        elif self.mode == DELIVERY:
            pos = self.grid_data.nearest_road(pos)
            if self.grid_data.get(pos) == DELIVERY:
                self.grid_data.erase(pos)
            else:
                self.grid_data.set_cell(pos, DELIVERY)
        elif self.mode == OBSTACLE:
            pos = self.grid_data.nearest_road(pos)
            self.grid_data.toggle_obstacle(pos)
        elif self.mode == WEIGHT:
            pos = self.grid_data.nearest_road(pos)
            self.grid_data.toggle_weight(pos)
        elif self.mode == EMPTY:
            self.grid_data.erase(pos)
        self.canvas.draw()
        self.update_stats()

    def run_route(self):
        if self.running:
            return
        self.grid_data.clear_path()
        self.canvas.draw()
        self.status_text.set("Calculating route")
        result = multi_route(self.grid_data, self.heuristic_choice.get())
        if not result["found"]:
            self.update_stats(result)
            self.status_text.set(result["message"])
            messagebox.showwarning("Route Problem", result["message"])
            return
        self.running = True
        self.status_text.set("Exploring map")
        self.animate_visited(result, 0)

    def animate_visited(self, result, index):
        visited = result["visited"]
        if index < len(visited):
            self.canvas.paint_temp(visited[index], VISITED)
            self.after(self.get_delay(), lambda: self.animate_visited(result, index + 1))
        else:
            self.status_text.set("Drawing route")
            self.canvas.start_route()
            self.animate_route(result, 1)

    def animate_route(self, result, index):
        path = result["path"]
        if index < len(path):
            self.canvas.draw_route_segment(path[index - 1], path[index])
            self.after(max(1, self.get_delay() // 2), lambda: self.animate_route(result, index + 1))
        else:
            self.canvas.repaint_path(path)
            self.running = False
            self.status_text.set("Route ready")
            self.update_stats(result)

    def clear_path(self):
        if self.running:
            return
        self.grid_data.clear_path()
        self.canvas.draw()
        self.status_text.set("Path cleared")
        self.update_stats()

    def reset_grid(self):
        if self.running:
            return
        self.grid_data.reset()
        self.canvas.draw()
        self.status_text.set("Grid reset")
        self.update_stats()

    def demo_map(self):
        if self.running:
            return
        self.grid_data.reset()
        self.grid_data.set_cell(self.grid_data.nearest_road((3, 2)), START)
        self.grid_data.set_cell(self.grid_data.nearest_road((5, 26)), DELIVERY)
        self.grid_data.set_cell(self.grid_data.nearest_road((16, 25)), DELIVERY)
        self.grid_data.set_cell(self.grid_data.nearest_road((18, 6)), DELIVERY)
        road_list = list(self.grid_data.road_cells or [])
        for pos in road_list[30:45]:
            self.grid_data.set_cell(pos, WEIGHT)
        self.canvas.draw()
        self.status_text.set("Demo map loaded")
        self.update_stats()

    def random_map(self):
        if self.running:
            return
        self.grid_data.reset()
        roads = list(self.grid_data.road_cells or [])
        if not roads:
            return
        random.shuffle(roads)
        self.grid_data.set_cell(roads[0], START)
        delivery_count = 4
        added = 0
        index = 1
        while added < delivery_count and index < len(roads):
            pos = roads[index]
            index += 1
            if self.grid_data.get(pos) == EMPTY:
                self.grid_data.set_cell(pos, DELIVERY)
                added += 1
        for pos in roads[index:index + 30]:
            if self.grid_data.get(pos) == EMPTY:
                self.grid_data.set_cell(pos, OBSTACLE)
        for pos in roads[index + 30:index + 55]:
            if self.grid_data.get(pos) == EMPTY:
                self.grid_data.set_cell(pos, WEIGHT)
        self.canvas.draw()
        self.status_text.set("Random map generated")
        self.update_stats()

    def update_stats(self, result=None):
        if not hasattr(self, "stats"):
            return
        if result:
            order = " -> ".join([f"({r},{c})" for r, c in result["order"]])
            nearest = " -> ".join([f"({r},{c})" for r, c in result.get("nearest_order", [])])
            text = (
                f"START        {self.grid_data.start}\n"
                f"DELIVERIES   {len(self.grid_data.deliveries)}\n"
                f"HEURISTIC    {result.get('heuristic', '-')}\n"
                f"TOTAL COST   {result['cost']}\n"
                f"NEAREST      {result.get('nearest_cost', 0)}\n"
                f"SAVED        {result.get('saved_cost', 0)}\n"
                f"PATH LEN     {len(result['path'])}\n"
                f"VISITED      {len(result['visited'])}\n"
                f"RUNTIME      {result['time']:.5f}s\n\n"
                f"OPTIMIZED\n{order if order else '-'}\n\n"
                f"NEAREST\n{nearest if nearest else '-'}"
            )
        else:
            text = (
                f"START        {self.grid_data.start}\n"
                f"DELIVERIES   {len(self.grid_data.deliveries)}\n"
                f"HEURISTIC    {self.heuristic_choice.get()}\n"
                f"TOTAL COST   0\n"
                f"NEAREST      0\n"
                f"SAVED        0\n"
                f"PATH LEN     0\n"
                f"VISITED      0\n"
                f"RUNTIME      0.00000s\n\n"
                f"OPTIMIZED\n-\n\n"
                f"NEAREST\n-"
            )
        self.stats.configure(state="normal")
        self.stats.delete("1.0", tk.END)
        self.stats.insert("1.0", text)
        self.stats.configure(state="disabled")
