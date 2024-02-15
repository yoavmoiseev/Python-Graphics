import logging
from tkinter import messagebox
from random import randrange
from datetime import datetime
import threading
import time
import tkinter as tk
import winsound


class Consts:
    """
    constant values for all classes
    """

    class Bullet:
        # bullets values
        max = 50
        speed = 10
        x0 = 0
        y0 = 0
        x1 = 5
        y1 = 15
        color = 'yellow'
        beep_frequency = 6000
        beep_duration = 5

    class Enemy:
        # Enemy values
        wait = 15  # millisecond
        speed = 20
        jump = 90
        color = 'black'
        start_x = 30
        start_y = 30
        wing_size = 25
        height = 20
        distance = 2
        max_num = 14
        screen_bottom_title = "Mission Failed"
        screen_bottom_message = "The enemy reached the screen bottom!"

    class Jet:
        # Jet values
        position_height_correction = 130
        color = 'blue'
        speed = 30
        wing_size = 40
        height = 25
        collision_title = 'You lose!'
        collision_message = 'Your collided with enemies, the jet will be destroyed!'
        collision_colors_list = ['pink', 'pink', 'red', 'red', 'yellow', 'yellow']

    class TkinterGames:
        # TkinterGames
        default_game = "Clicker"
        all_colors = ["red", "green", "blue", "orange", "purple"]
        milliseconds = 0
        title = "Tkinter Games"
        choose_game_label = "Choose Game"
        first_game_name = "Clicker"
        second_game_name = "Catch the button"
        third_game_name = "Space Invaders"
        first_game_button_text = "Click me"
        second_game_button_text = "Catch Me"
        timer_label = "Timer"
        timer_index = 3
        timer_wait = 100
        third_game_label = "Bullets-"
        third_game_index = 4
        button_beep_frequency = 1000
        button_beep_duration = 30

    class Log:
        # logging messages
        unreachable = "The enemy object is unreachable"
        file = 'TkinterGames.log'
        prefix = ":   -"
        suffix = "-   successfully started"
        unreachable = "Jet object is unreachable"
        game_over = "The jet destroyed, the game is over!!!"
        win_info = "The -winfo_height()- fails, using -winfo_screenheight()- instead"

    class Sound:
        shoot_file_name = "shoot.wav"
        exploded_file_name = "enemy_exploded.wav"
        injured_file_name = "jet-injured.wav"

    class Others:
        screen_correction_y = 40
        fore_ground_color = "white"


class Jet:
    """
    triangle that represent gamers airplane/jet
    """

    def __init__(self, root, canvas, color):
        self._root = root
        self._canvas = canvas
        self._color = color
        self.color_index = -1
        self.color_list = Consts.Jet.collision_colors_list
        y1 = root.winfo_screenheight() - Consts.Jet.position_height_correction
        x1 = root.winfo_screenwidth() // 2
        self.jet = canvas.create_polygon(x1, y1, x1 + Consts.Jet.wing_size,
                                         y1 + Consts.Jet.height,
                                         x1 - Consts.Jet.wing_size, y1 + Consts.Jet.height,
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
            messagebox.showerror(Consts.Jet.collision_title, Consts.Jet.collision_message)
            self._canvas.delete(self.jet)
            return -1
        else:
            self._canvas.itemconfig(self.jet, fill=self.color_list[self.color_index])
            return self.color_index


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


class StarWars:
    """
    Star-Wars game, a triangle moved over canvas and shoots on objects that above him
    """

    def __init__(self, root, menu_bar_counter):
        self.root = root
        self.root.title(Consts.TkinterGames.third_game_name)
        self.after_flag = False
        self.canvas = tk.Canvas(self.root, width=root.winfo_screenwidth(),
                                height=root.winfo_screenheight())
        self.canvas.pack()
        self.label_counter = menu_bar_counter

        self.jet = Jet(root=self.root, canvas=self.canvas, color=Consts.Jet.color)

        self.bullet_list = []
        self.enemies_list = []

        # Bind key presses to the key_event function
        self.root.bind("<KeyPress>", self.key_event)

        self.num_of_bullets = Consts.Bullet.max

        self.move_the_bullet()

        self.create_enemies(1, Consts.Enemy.max_num + 1)

        self.move_enemy()

        self.root.mainloop()

    # ----------------------------------------------------------------------------------------------------------

    def create_enemies(self, begin=1, end=20):
        for i in range(begin, end):
            self.add_enemy(Consts.Enemy.start_x + Consts.Enemy.wing_size * 2 * i * Consts.Enemy.distance)

    def key_event(self, event):
        """
        Controlling the jet with keyboard
        :param event:
        :return:
        """
        key = event.keysym
        if key == 'Up':
            # Move the triangle up
            self.canvas.move(self.jet(), 0, -Consts.Jet.speed)
        elif key == 'Down':
            self.canvas.move(self.jet(), 0, Consts.Jet.speed)
        elif key == 'Left':
            self.canvas.move(self.jet(), -Consts.Jet.speed, 0)
        elif key == 'Right':
            self.canvas.move(self.jet(), Consts.Jet.speed, 0)
        elif key == 'space':
            self.bullet(self.label_counter,
                        Consts.TkinterGames.third_game_index)

    def bullet(self, menu_label_counter, label_index):
        """
        Creates the bullet on the jet apex
        :return: returns 0 if out of bullets
        """
        if self.num_of_bullets == 0:
            return 0

        self.num_of_bullets -= 1
        menu_label_counter.entryconfig(label_index,
                                       label=Consts.TkinterGames.third_game_label
                                             + str(self.num_of_bullets))

        # The first argument is the frequency, and the second is the duration in milliseconds
        winsound.PlaySound(Consts.Sound.shoot_file_name, 1)

        new_bullet = self.canvas.create_oval(Consts.Bullet.x0, Consts.Bullet.y0,
                                             Consts.Bullet.x1, Consts.Bullet.y1,
                                             fill=Consts.Bullet.color)
        x1 = self.canvas.coords(self.jet())[0]
        y1 = self.canvas.coords(self.jet())[1]
        self.canvas.move(new_bullet, x1, y1)
        self.bullet_list.append(new_bullet)

    def move_the_bullet(self):
        """
        move the bullets shut from jet, up over the screen
        :return:
        """
        for bullet in self.bullet_list:
            self.canvas.move(bullet, 0, -Consts.Bullet.speed)

            y1 = self.canvas.coords(bullet)[1]
            # up screen reached
            if y1 < 1:
                self.bullet_list.remove(bullet)
                self.canvas.delete(bullet)
        # Sleep
        self.root.after(Consts.Enemy.wait, lambda: self.move_the_bullet())

    def add_enemy(self, left_x=Consts.Enemy.start_x, left_y=Consts.Enemy.start_y,
                  color=Consts.Enemy.color):
        new_enemy = Enemy(self.canvas, left_x, left_y, color)
        self.enemies_list.append(new_enemy)

    def died(self, enemy):
        """
        checks if enemy had been hit by bullet
        :param enemy:
        :return:
        """
        for bullet in self.bullet_list:
            enemy_x1 = self.canvas.coords(enemy.polygon)[0]
            enemy_y1 = self.canvas.coords(enemy.polygon)[1]
            enemy_x2 = self.canvas.coords(enemy.polygon)[2]
            enemy_y2 = self.canvas.coords(enemy.polygon)[3]
            enemy_x3 = self.canvas.coords(enemy.polygon)[4]
            enemy_y3 = self.canvas.coords(enemy.polygon)[5]

            bullet_x1 = self.canvas.coords(bullet)[0]
            bullet_y1 = self.canvas.coords(bullet)[1]
            bullet_x2 = self.canvas.coords(bullet)[2]
            bullet_y2 = self.canvas.coords(bullet)[3]

            bullet_x_mid = (bullet_x1 + bullet_x2) // 2
            bullet_y_mid = (bullet_y1 + bullet_y2) // 2

            # if the bullet inside the triangle area
            # the enemy triangle assumed as rectangle
            if enemy_y1 >= bullet_y_mid >= enemy_y2 and \
                    enemy_x2 >= bullet_x_mid >= enemy_x3:
                self.canvas.delete(bullet)
                self.bullet_list.remove(bullet)
                return True
        return False

    def jet_collided(self, enemy):
        """
        checks if jet collide with enemy
        :param enemy:
        :return:
        """
        try:
            enemy_x1 = self.canvas.coords(enemy.polygon)[0]
            enemy_y1 = self.canvas.coords(enemy.polygon)[1]
            enemy_x2 = self.canvas.coords(enemy.polygon)[2]
            enemy_y2 = self.canvas.coords(enemy.polygon)[3]
            enemy_x3 = self.canvas.coords(enemy.polygon)[4]
            enemy_y3 = self.canvas.coords(enemy.polygon)[5]

            jet_x1 = self.canvas.coords(self.jet())[0]
            jet_y1 = self.canvas.coords(self.jet())[1]
            jet_x2 = self.canvas.coords(self.jet())[2]
            jet_y2 = self.canvas.coords(self.jet())[3]
            jet_x3 = self.canvas.coords(self.jet())[4]
            jet_y3 = self.canvas.coords(self.jet())[5]

            # Checks collision of three jet apexes with enemy triangle
            # the enemy triangle assumed as rectangle
            if enemy_y1 >= jet_y1 >= enemy_y2 and enemy_x1 <= jet_x1 <= enemy_x2 \
                    or \
                    enemy_y1 >= jet_y2 >= enemy_y2 and enemy_x1 <= jet_x2 <= enemy_x2 \
                    or \
                    enemy_y1 >= jet_y3 >= enemy_y2 and enemy_x1 <= jet_x3 <= enemy_x2:
                return True
            return False
            return False
        except:
            logging.warning(Consts.log_unreachable)
            return False

    def move_enemy(self):
        """
        move enemies horizontally,
        drop down to the next line when the end of the screen reached
        checks collision with other objects
        :return: 0 when the jet destroyed

        """
        for enemy in self.enemies_list:
            if self.jet_collided(enemy):
                winsound.PlaySound(Consts.Sound.injured_file_name, 1)
                #            the jet destroyed
                if self.jet.next_color() == -1:
                    logging.info(Consts.Log.game_over)
                    return 0  # Stop moving enemies

            try:
                enemy_x1 = self.canvas.coords(enemy.polygon)[0]
                # right window corner reached
                if enemy_x1 >= self.root.winfo_width() - Consts.Others.screen_correction_y:
                    enemy.direction = -1
                    self.canvas.move(enemy.polygon, (-Consts.Enemy.speed), Consts.Enemy.jump)
                # left window corner reached
                elif enemy_x1 <= Consts.Others.screen_correction_y:
                    enemy.direction = 1
                    self.canvas.move(enemy.polygon, Consts.Enemy.speed, Consts.Enemy.jump)
                else:
                    self.canvas.move(enemy.polygon, Consts.Enemy.speed * enemy.direction, 0)

                #  if the winfo_height() returns correct values?
                #  returns 1 when used immediately after canvas creation,
                #  instead of real size
                if self.canvas.winfo_height() > 1:
                    bottom = self.canvas.winfo_height()
                else:
                    bottom = self.root.winfo_screenheight()
                    # logging.warning(Consts.log_win_info)

                enemy_y1 = self.canvas.coords(enemy.polygon)[1]
                # screen bottom reached
                if enemy_y1 > bottom:
                    messagebox.showerror(Consts.Enemy.screen_bottom_title, Consts.Enemy.screen_bottom_message)
                    return ()

                if self.died(enemy):
                    self.enemies_list.remove(enemy)
                    self.canvas.delete(enemy.polygon)
                    winsound.PlaySound(Consts.Sound.exploded_file_name, 1)
            except:
                logging.error(Consts.Log.unreachable)

        self.root.after(Consts.Enemy.wait, lambda: self.move_enemy())


class TkinterGames:
    """
    Creates a graphic window with a menu for selecting games
    """

    def __init__(self, game_selected=Consts.TkinterGames.default_game):
        """
        constructor, builds the main window with the menus and "Click Me" button
        """
        logging.basicConfig(filename=Consts.Log.file, level=logging.DEBUG,
                            format='%(levelname)s - %(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logging.info(Consts.Log.prefix + game_selected +
                     Consts.Log.suffix)

        self.choose_game_menu = game_selected
        self.selected_game = game_selected
        self.color_index = 0
        self.all_colors = Consts.TkinterGames.all_colors
        self.milliseconds = Consts.TkinterGames.milliseconds

        self.root = tk.Tk()
        self.root.title(Consts.TkinterGames.title)
        self.root.wm_state("zoomed")

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.create_choose_game_menu()

        # shifting the stopper to the middle
        shift = self.root.winfo_screenheight() // 4
        self.menu_bar.add_command(label=' ' * shift, state=tk.DISABLED)

        self.menu_bar.add_command(label=Consts.TkinterGames.timer_label, state=tk.DISABLED)
        self.stop_watch()

        self.catch_me_button = None

        # Star Wars game started
        if self.selected_game == Consts.TkinterGames.third_game_name:
            self.menu_bar.add_command(label=Consts.TkinterGames.third_game_label
                                            + str(Consts.Bullet.max), state=tk.DISABLED)
            StarWars(self.root, self.menu_bar)
        else:
            self.create_catch_me_button()
            self.catch_me_button.bind("<Enter>", self.on_mouse_on)

        # Only commands up here will be displayed/executed
        self.root.mainloop()

    def create_choose_game_menu(self):
        """
        :return:
        """
        # Create a "Choose Game" menu
        self.choose_game_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=Consts.TkinterGames.choose_game_label, menu=self.choose_game_menu)
        self.add_choices_to_menu()

    def stop_watch(self):
        """
        creating stopper label inside the window to display: minutes, seconds and milliseconds from game beginning
        :return:
        """
        self.milliseconds += 1

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

        stopper_str = minutes + ":" + seconds + ":" + str(self.milliseconds % 10) + '0'

        self.menu_bar.entryconfig(Consts.TkinterGames.timer_index, label=stopper_str)
        self.menu_bar.after(Consts.TkinterGames.timer_wait, self.stop_watch)

    def create_catch_me_button(self):
        button_text = ""
        # Create a button with text according to menu selected
        # and place it in the window
        if self.selected_game == Consts.TkinterGames.first_game_name:
            button_text = Consts.TkinterGames.first_game_button_text
        elif self.selected_game == Consts.TkinterGames.second_game_name:
            button_text = Consts.TkinterGames.second_game_button_text

        self.catch_me_button = tk.Button(self.root, text=button_text, command=self.on_button_click)
        self.catch_me_button.pack(pady=20)

    # Function to be called when the button is clicked
    def on_button_click(self):
        self.color_index += 1
        self.catch_me_button.config(bg=self.all_colors[self.color_index % len(self.all_colors)],
                                    fg=Consts.Others.fore_ground_color,
                                    text=str(self.color_index))

        self.catch_me_button.place(x=randrange(self.root.winfo_width() - self.catch_me_button.winfo_width()),
                                   y=randrange(self.root.winfo_height()) - self.catch_me_button.winfo_height())

    # on mouse over event
    def on_mouse_on(self, event):
        """
        event that triggered when mouse on this button
        :param event: event that send by OS when mouse on
        :return: No return value
        """
        if self.selected_game != Consts.TkinterGames.second_game_name:
            return

        self.color_index += 1
        self.catch_me_button.config(bg=self.all_colors[self.color_index % len(self.all_colors)],
                                    fg=Consts.Others.fore_ground_color, text=str(self.color_index))

        self.catch_me_button.place(x=randrange(self.root.winfo_width() - self.catch_me_button.winfo_width()),
                                   y=randrange(self.root.winfo_height()) - self.catch_me_button.winfo_height())
        winsound.Beep(Consts.TkinterGames.button_beep_frequency, Consts.TkinterGames.button_beep_duration)

    # =========================Start of "Game Menu"===================================================
    # Function to be called when a menu item is selected
    def menu_choice(self, choice):
        """
            function to start the games according to selection in menu
            :param choice:
            :return:
            """
        if choice == Consts.TkinterGames.first_game_name:
            self.root.destroy()
            self.__init__(Consts.TkinterGames.first_game_name)
        elif choice == Consts.TkinterGames.second_game_name:
            self.root.destroy()
            self.__init__(Consts.TkinterGames.second_game_name)
        elif choice == Consts.TkinterGames.third_game_name:
            self.root.destroy()
            self.__init__(Consts.TkinterGames.third_game_name)

    def reset_timer(self):
        self.milliseconds = 0

    def add_choices_to_menu(self):
        # Add choices to the "choose_game" menu
        self.choose_game_menu.add_command(label=Consts.TkinterGames.first_game_name,
                                          command=lambda: self.menu_choice(Consts.TkinterGames.first_game_name))
        self.choose_game_menu.add_command(label=Consts.TkinterGames.second_game_name,
                                          command=lambda: self.menu_choice(Consts.TkinterGames.second_game_name))
        self.choose_game_menu.add_command(label=Consts.TkinterGames.third_game_name,
                                          command=lambda: self.menu_choice(Consts.TkinterGames.third_game_name))
        self.choose_game_menu.add_separator()  # Add a separator line
        # ============= end of "Game Menu"==========================================================


if __name__ == "__main__":
    create_window = TkinterGames()
