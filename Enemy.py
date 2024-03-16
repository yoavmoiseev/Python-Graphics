import consts
import tkinter as tk


class Enemy:
    """
    Create an enemy-triangle with the apex downwards
    """

    def __init__(self, canvas: tk.Canvas, left_x=consts.Enemy.start_x,
                 left_y=consts.Enemy.start_y, color=consts.Enemy.color):
        self.polygon = canvas.create_polygon(left_x, left_y,
                                             left_x + consts.Enemy.wing_size,
                                             left_y - consts.Enemy.height,
                                             left_x - consts.Enemy.wing_size,
                                             left_y - consts.Enemy.height,
                                             fill=color)
        # from left to right
        self.direction = 1

    def __call__(self):
        return self.polygon
