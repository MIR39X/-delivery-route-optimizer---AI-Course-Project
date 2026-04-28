import tkinter as tk


class SlidingSelector(tk.Canvas):
    def __init__(self, master, values, variable, command=None):
        super().__init__(master, height=32, bg="#f8fafc", highlightthickness=0, bd=0)
        self.values = values
        self.variable = variable
        self.command = command
        self.pos = 0
        self.bind("<Button-1>", self.clicked)
        self.bind("<Configure>", lambda event: self.redraw())
        self.after(30, self.redraw)

    def clicked(self, event):
        width = max(1, self.winfo_width())
        index = int(event.x / (width / len(self.values)))
        index = max(0, min(index, len(self.values) - 1))
        self.variable.set(self.values[index])
        self.animate_to(index)
        if self.command:
            self.command(self.values[index])

    def active_index(self):
        value = self.variable.get()
        if value in self.values:
            return self.values.index(value)
        self.variable.set(self.values[0])
        return 0

    def rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def redraw(self):
        self.delete("all")
        width = max(1, self.winfo_width())
        height = max(1, self.winfo_height())
        count = len(self.values)
        part = width / count
        index = self.active_index()
        self.pos = index

        self.rounded_rect(0, 0, width, height, 8, fill="#9aa1a6", outline="")
        self.rounded_rect(index * part + 3, 3, (index + 1) * part - 3, height - 3, 7, fill="#3b91d9", outline="")

        for i, value in enumerate(self.values):
            x = i * part + part / 2
            self.create_text(x, height / 2, text=value, fill="white", font=("Segoe UI", 9))

    def animate_to(self, index):
        self.slide(float(self.pos), float(index), 0)

    def slide(self, current, target, step):
        width = max(1, self.winfo_width())
        height = max(1, self.winfo_height())
        count = len(self.values)
        part = width / count
        new_pos = current + (target - current) * 0.35

        self.delete("all")
        self.rounded_rect(0, 0, width, height, 8, fill="#9aa1a6", outline="")
        self.rounded_rect(new_pos * part + 3, 3, (new_pos + 1) * part - 3, height - 3, 7, fill="#3b91d9", outline="")

        for i, value in enumerate(self.values):
            x = i * part + part / 2
            self.create_text(x, height / 2, text=value, fill="white", font=("Segoe UI", 9))

        if abs(new_pos - target) > 0.003 and step < 18:
            self.after(12, lambda: self.slide(new_pos, target, step + 1))
        else:
            self.pos = target
            self.redraw()
