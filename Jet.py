import consts
from tkinter import messagebox


class Jet:
    """
    triangle that represent the player airplane/jet
    """

    def __init__(self, root, canvas, color):
        self._root = root
        self._canvas = canvas
        self._color = color
        self.color_index = -1
        self.color_list = consts.Jet.collision_colors_list
        y1 = root.winfo_screenheight() - consts.Jet.position_height_correction
        x1 = root.winfo_screenwidth() // 2
        self.jet = canvas.create_polygon(x1, y1, x1 + consts.Jet.wing_size,
                                         y1 + consts.Jet.height,
                                         x1 - consts.Jet.wing_size, y1 + consts.Jet.height,
                                         fill=color)

    def __call__(self):
        return self.jet

    def next_color(self):
        """
        changes jet colors after collision with enemy
        :return:
        """
        self.color_index += 1
        if self.color_index >= len(self.color_list):
            return -1
        else:
            self._canvas.itemconfig(self.jet, fill=self.color_list[self.color_index])
            return self.color_index
