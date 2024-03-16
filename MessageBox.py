import tkinter as tk


class MessageBox:
    def __init__(self, root, title, my_text):
        new_window = tk.Toplevel(root)
        new_window.title(title)
        label = tk.Label(new_window, text=my_text, justify='right')
        new_window.attributes('-toolwindow', 1)
        label.pack()
