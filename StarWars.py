from tkinter import messagebox
from random import randrange
from datetime import datetime
import threading
import time
import tkinter as tk
from tkinter import ttk


class Consts:
    """
    constant values for Star_wars class
    """
    jet_speed = 30
    bullet_speed = 10
    enemy_wait = 10  # millisecond
    enemy_jump = 100
    max_bullets = 50


class Jet:
    """
    triangle that represent my airplane/jet
    """
    def __init__(self, root, canvas, color='green'):
        self._root = root
        self._canvas = canvas
        self._color = color
        self.color_index = -1
        self.color_list = ['pink', 'pink', 'red', 'red', 'yellow', 'yellow']
        self.jet = canvas.create_polygon(root.winfo_screenheight() / 2, 700, root.winfo_screenheight() / 2
                                         + 50, 750, root.winfo_screenheight() / 2 - 50, 750, fill=color)

    def __call__(self):
        return self.jet

    def next_color(self):
        """
        changes jet colors after collision with enemy
        :return:
        """
        self.color_index += 1
        if self.color_index >= len(self.color_list):
            messagebox.showerror('You lose!', 'Your jet will be destroyed!')
            self._canvas.delete(self.jet)
        else:
            self._canvas.itemconfig(self.jet, fill=self.color_list[self.color_index])


class Enemy:
    """
    Create an enemy-triangle with the apex downwards
    """
    def __init__(self, canvas: tk.Canvas, left_x=30, left_y=30, color='black'):
        self.polygon = canvas.create_polygon(left_x, left_y, left_x + 25, left_y - 20, left_x - 25, left_y - 20,
                                             fill=color)
        self.direction = 1  # from left to right


class StarWars:
    """
    Star-Wars game, a triangle moved over canvas and shoot on objects that above him
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Space Invaders")
        self.after_flag = False
        self.canvas = tk.Canvas(self.root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        self.canvas.pack()

        self.jet = Jet(root=self.root, canvas=self.canvas, color='blue')

        self.bullet_list = []
        self.enemies_list = []

        # Bind key presses to the key_event function
        self.root.bind("<KeyPress>", self.key_event)

        self.move_the_bullet()

        self.create_enemies(1, 25)

        self.move_enemy()

        self.num_of_bullets = Consts.max_bullets

        self.root.mainloop()

    # ----------------------------------------------------------------------------------------------------------

    def create_enemies(self, begin=1, end=20):
        for i in range(begin, end):
            self.add_enemy(30 + 60 * i)

    def key_event(self, event):
        key = event.keysym
        if key == 'Up':
            self.canvas.move(self.jet(), 0, -Consts.jet_speed)  # Move the triangle up
        elif key == 'Down':
            self.canvas.move(self.jet(), 0, Consts.jet_speed)
        elif key == 'Left':
            self.canvas.move(self.jet(), -Consts.jet_speed, 0)
        elif key == 'Right':
            self.canvas.move(self.jet(), Consts.jet_speed, 0)
        elif key == 'space':
            self.bullet()

    def bullet(self):
        if self.num_of_bullets == 0:
            return ()
        self.num_of_bullets -= 1
        new_bullet = self.canvas.create_oval(0, 0, 5, 15, fill='yellow')
        self.canvas.move(new_bullet, self.canvas.coords(self.jet())[0],
                         self.canvas.coords(self.jet())[1])
        self.bullet_list.append(new_bullet)

    def move_the_bullet(self):
        """
        move the bullets shut from jet, up over the screen
        :return:
        """
        for bullet in self.bullet_list:
            self.canvas.move(bullet, 0, -Consts.bullet_speed)
            #  up screen reached
            if self.canvas.coords(bullet)[1] < 1:
                self.bullet_list.remove(bullet)
                self.canvas.delete(bullet)
        # Sleep
        self.root.after(Consts.enemy_wait, lambda: self.move_the_bullet())

    def add_enemy(self, left_x=30, left_y=30, color='black'):
        new_enemy = Enemy(self.canvas, left_x, left_y)
        self.enemies_list.append(new_enemy)

    def enemy_died(self, enemy):
        """
        checks if hit by bullet
        :param enemy:
        :return:
        """
        for bullet in self.bullet_list:
            #                           Y1                               Y1                              Y2
            if self.canvas.coords(enemy.polygon)[1] >= self.canvas.coords(bullet)[1] >= \
                    self.canvas.coords(enemy.polygon)[3] and \
                    self.canvas.coords(enemy.polygon)[0] <= self.canvas.coords(bullet)[0] <= \
                    self.canvas.coords(enemy.polygon)[2]:
                self.canvas.delete(bullet)
                self.bullet_list.remove(bullet)
                return True
        return False

    def jet_collision(self, enemy):
        """
        checks if jet collide with enemy
        :param enemy:
        :return:
        """
        #                           Y1                               Y1                              Y2
        if self.canvas.coords(enemy.polygon)[1] >= self.canvas.coords(self.jet())[1] >= \
                self.canvas.coords(enemy.polygon)[3] and \
                self.canvas.coords(enemy.polygon)[0] <= self.canvas.coords(self.jet())[0] <= \
                self.canvas.coords(enemy.polygon)[2]:
            self.jet.next_color()
            return True
        return False

    def move_enemy(self):
        """
        move objects horizontally,
         drop down to the next line when the end of the screen reached
        :return:
        """
        for enemy in self.enemies_list:
            enemy: Enemy
            self.jet_collision(enemy)
            # right window corner reached
            if self.canvas.coords(enemy.polygon)[0] >= self.root.winfo_width() - 40:
                enemy.direction = -1
                self.canvas.move(enemy.polygon, (-Consts.bullet_speed), Consts.enemy_jump)
            # left window corner reached
            elif self.canvas.coords(enemy.polygon)[0] <= 40:
                enemy.direction = 1
                self.canvas.move(enemy.polygon, Consts.bullet_speed, Consts.enemy_jump)
            else:
                self.canvas.move(enemy.polygon, Consts.bullet_speed * enemy.direction, 0)

            # screen button reached       self.root.winfo_screenheight() self.canvas.winfo_height()
            if self.canvas.winfo_height() > 1:
                bottom = self.canvas.winfo_height()
            else:
                bottom = self.root.winfo_screenheight()
            if self.canvas.coords(enemy.polygon)[1] > bottom:
                messagebox.showerror("Mission Failed", "The enemy reached the screen button!")
                return ()

            if self.enemy_died(enemy):
                self.enemies_list.remove(enemy)
                self.canvas.delete(enemy.polygon)

        self.root.after(Consts.enemy_wait, lambda: self.move_enemy())


class TkinterGames:
    """
    Creates a graphic window with a menu for selecting games
    """
    def __init__(self, game_selected="Clicker"):
        """
        constructor, builds the main window with the menus and "Click Me" button
        """
        self.choose_game_menu = game_selected
        self.selected_game = game_selected
        self.color_index = 0
        self.all_colors = ["red", "green", "blue", "orange", "purple"]
        self.milliseconds = 0

        self.root = tk.Tk()
        self.root.title("tkinter games")
        self.root.wm_state("zoomed")

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.create_choose_game_menu()
        self.stopper_label = tk.Label(self.root, text="00:00:00")

        # Star Wars game started
        if self.selected_game == "Star Wars":
            StarWars(self.root)
        else:
            # !!!BUG when destroying the window
            self.stop_watch()
            self.create_catch_me_button()
            self.catch_me_button.bind("<Enter>", self.on_mouse_on)
            self.stopper_label.pack()

        # Only commands up here will be displayed/executed
        self.root.mainloop()

    def create_choose_game_menu(self):
        """
        :return:
        """
        # Create a "Choose Game" menu
        self.choose_game_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Choose Game", menu=self.choose_game_menu)
        self.add_choices_to_menu()

    def stop_watch(self):
        """
        creating stopper label inside the window to display seconds from game beginning
        :return:
        """
        self.milliseconds += 1
        self.stopper_label.after(100, self.stop_watch)
        minutes = self.milliseconds // 600
        if minutes < 10:
            minutes = '0' + str(minutes)
        else:
            minutes = str(minutes)

        seconds = self.milliseconds // 10 % 60
        if seconds <= 9:
            seconds = '0' + str(seconds)
        else:
            seconds = str(seconds)
        self.stopper_label.config(text=minutes + ":" + seconds
                                       + ":" + str(self.milliseconds % 10) + '0')

    def create_catch_me_button(self):
        # Create a button with text according to menu selected
        # and place it in the window
        if self.selected_game == "Clicker":
            button_text = "Click me"
        elif self.selected_game == "Catch the button":
            button_text = "Catch Me"
        else:
            button_text = ""

        self.catch_me_button = tk.Button(self.root, text=button_text, command=self._on_button_click)
        self.catch_me_button.pack(pady=20)

    # Function to be called when the button is clicked
    def _on_button_click(self):
        self.color_index += 1
        self.catch_me_button.config(bg=self.all_colors[self.color_index % len(self.all_colors)], fg="white",
                                    text=str(self.color_index))
        # Use the pack geometry manager to place the button at the top of the window
        self.catch_me_button.place(x=randrange(10, self.root.winfo_width() - self.catch_me_button.winfo_width()),
                                   y=randrange(10, self.root.winfo_height()) - self.catch_me_button.winfo_height())

    # on mouse over event
    def on_mouse_on(self, event):
        """
        event that triggered when mouse on this button
        :param event: event that send by OS when mouse on
        :return: No return value
        """
        if self.selected_game != "Catch the button":
            return
        self.color_index += 1
        self.catch_me_button.config(bg=self.all_colors[self.color_index % len(self.all_colors)], fg="white",
                                    text=str(self.color_index))

        # Use the pack geometry manager to place the button at the top of the window
        self.catch_me_button.place(x=randrange(10, self.root.winfo_width() - self.catch_me_button.winfo_width()),
                                   y=randrange(10, self.root.winfo_height()) - self.catch_me_button.winfo_height())

    def reset_button_click(self):
        self.create_catch_me_button()
        self.catch_me_button.bind("<Enter>", self.on_mouse_on)

    # =========================Start of "Game Menu"===================================================
    # Function to be called when a menu item is selected
    def menu_choice(self, choice):
        """
            function to start the games according to selection in menu
            :param choice:
            :return:
            """
        if choice == "Clicker":
            self.root.destroy()
            self.__init__("Clicker")
        elif choice == "Catch the button":
            self.root.destroy()
            self.__init__("Catch the button")
        elif choice == "Star Wars":
            self.root.destroy()
            self.__init__("Star Wars")

        elif choice == "Reset Score":
            self.selected_game = "Reset Score"
            self.reset_button_click()

    def reset_timer(self):
        self.milliseconds = 0

    def add_choices_to_menu(self):
        # Add choices to the "choose_game" menu
        self.choose_game_menu.add_command(label="Clicker", command=lambda: self.menu_choice("Clicker"))
        self.choose_game_menu.add_command(label="Catch the button",
                                          command=lambda: self.menu_choice("Catch the button"))
        self.choose_game_menu.add_command(label="Star Wars",
                                          command=lambda: self.menu_choice("Star Wars"))
        self.choose_game_menu.add_separator()  # Add a separator line

        # ============= end of "Game Menu"==========================================================


if name == "main":
    create_window = TkinterGames()
