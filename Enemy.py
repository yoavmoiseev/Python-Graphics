from Consts import *
import tkinter as tk


class Enemy:
    """
    Create an enemy-triangle with the apex downwards
    """

    def __init__(self, canvas: tk.Canvas, left_x=Consts.Enemy.start_x,
                 left_y=Consts.Enemy.start_y, color=Consts.Enemy.color):
        self.polygon = canvas.create_polygon(left_x, left_y,
                                             left_x + Consts.Enemy.wing_size,
                                             left_y - Consts.Enemy.height,
                                             left_x - Consts.Enemy.wing_size,
                                             left_y - Consts.Enemy.height,
                                             fill=color)
        # from left to right
        self.direction = 1

    def __call__(self):
        return self.polygon
