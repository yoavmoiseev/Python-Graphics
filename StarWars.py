import tkinter as tk
from tkinter import messagebox
import logging

import sound
from Consts import *
from Jet import *
from Enemy import *


class StarWars:
    """
    Star-Wars game, a triangle moved over canvas and shoots on objects that above him
    """

    def __init__(self, root, menu_bar, callback, level):

        self.root = root
        self.callback = callback
        self.level = level
        self.root.title(Consts.TkinterGames.third_game_name)
        self.after_flag = False
        self.canvas = tk.Canvas(self.root, width=root.winfo_screenwidth(),
                                height=root.winfo_screenheight())
        self.canvas.pack()

        self.num_of_bullets = Consts.Bullet.max - self.level * 2
        menu_bar.add_command(label=Consts.TkinterGames.third_game_label
                             + str(self.num_of_bullets), state=tk.DISABLED)
        self.menu_bar = menu_bar

        self.level_label = menu_bar.add_command(label=Consts.TkinterGames.level_label
                                                + str(level), state=tk.DISABLED)

        self.jet = Jet(root=self.root, canvas=self.canvas, color=Consts.Jet.color)

        self.bullet_list = []
        self.enemies_list = []

        # Bind key presses to the key_event function
        self.key_event_id = self.root.bind(Consts.StarWars.key_event, self.key_event)

        self.move_the_bullet()

        self.create_enemies(1, Consts.Enemy.max_num + 1)

        self.move_enemy()

        self.root.mainloop()

    # ----------------------------------------------------------------------------------------------------------

    def create_enemies(self, begin=1, end=20):
        for i in range(begin, end):
            self.add_enemy(Consts.Enemy.start_x + Consts.Enemy.wing_size * 2 * i * Consts.Enemy.distance)

    def clear_screen_objects(self):
        for bullet in self.bullet_list:
            self.canvas.delete(bullet)

        for enemy in self.enemies_list:
            self.canvas.delete(enemy())

        if self.jet is not None:
            self.canvas.delete(self.jet())

        # Bind key presses to the key_event function
        self.root.unbind(Consts.StarWars.key_event, self.key_event_id)

    def key_event(self, event):
        """
        Controlling the jet with keyboard
        :param event:
        :return:
        """
        key = event.keysym
        if key == Consts.StarWars.move_up_key:
            # Move the triangle up
            self.canvas.move(self.jet(), 0, -Consts.Jet.speed)
        elif key == Consts.StarWars.move_down_key:
            self.canvas.move(self.jet(), 0, Consts.Jet.speed)
        elif key == Consts.StarWars.move_left_key:
            self.canvas.move(self.jet(), -Consts.Jet.speed, 0)
        elif key == Consts.StarWars.move_right_key:
            self.canvas.move(self.jet(), Consts.Jet.speed, 0)

        elif key == Consts.StarWars.shoot_key:
            self.bullet(self.menu_bar,
                        Consts.TkinterGames.third_game_index)

    def bullet(self, menu_label_counter, label_index):
        """
        Creates the bullet on the jet apex
        :return: returns 0 if out of bullets
        """
        if self.num_of_bullets == 0:
            return 0

        self.num_of_bullets -= 1
        menu_label_counter.entryconfig(label_index, label=Consts.TkinterGames.third_game_label
                                       + str(self.num_of_bullets))

        sound.play_sound(Consts.Sound.shoot_file_name, 1)

        new_bullet = self.canvas.create_oval(Consts.Bullet.x0, Consts.Bullet.y0,
                                             Consts.Bullet.x1, Consts.Bullet.y1,
                                             fill=Consts.Bullet.color)
        try:
            x1 = self.canvas.coords(self.jet())[0]
            y1 = self.canvas.coords(self.jet())[1]
            self.canvas.move(new_bullet, x1, y1)
            self.bullet_list.append(new_bullet)
        except Exception as exc_type:
            logging.exception(f"{type(exc_type).__name__}: {exc_type}")

    def move_the_bullet(self):
        """
        move the bullets shut from jet, up over the screen
        :return:
        """
        try:
            for bullet in self.bullet_list:
                self.canvas.move(bullet, 0, -Consts.Bullet.speed)

                y1 = self.canvas.coords(bullet)[1]
                # up screen reached
                if y1 < 1:
                    self.bullet_list.remove(bullet)
                    self.canvas.delete(bullet)
        except Exception as exc_type:
            logging.exception(f"{type(exc_type).__name__}: {exc_type}")

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
            try:
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
            except Exception as exc_type:
                logging.exception(f"{type(exc_type).__name__}: {exc_type}")

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
        except Exception as exc_type:
            logging.exception(f"{type(exc_type).__name__}: {exc_type}")

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
                sound.play_sound(Consts.Sound.jet_injured_file_name, 1)
                #            the jet destroyed
                if self.jet.next_color() == -1:
                    self.clear_screen_objects()
                    messagebox.showerror(Consts.Jet.collision_title, Consts.Jet.collision_message)
                    logging.info(Consts.Log.game_over)
                    return self.callback('jet_collided')
            try:
                enemy_x1 = self.canvas.coords(enemy.polygon)[0]
                # right window corner reached
                if enemy_x1 >= self.root.winfo_width() - Consts.Others.screen_correction_y:
                    enemy.direction = -1
                    self.canvas.move(enemy.polygon, (-Consts.Enemy.speed) - self.level * 2,
                                     Consts.Enemy.jump)
                # left window corner reached
                elif enemy_x1 <= Consts.Others.screen_correction_y:
                    enemy.direction = 1
                    self.canvas.move(enemy.polygon, Consts.Enemy.speed + self.level * 2,
                                     Consts.Enemy.jump)
                else:
                    self.canvas.move(enemy.polygon, (Consts.Enemy.speed + self.level * 2)
                                     * enemy.direction, 0)

                #  if the winfo_height() returns correct values?
                #  returns 1 when used immediately after canvas creation,
                #  instead of real size
                if self.canvas.winfo_height() > 1:
                    bottom = self.canvas.winfo_height()
                else:
                    bottom = self.root.winfo_screenheight()

                enemy_y1 = self.canvas.coords(enemy.polygon)[1]
                # screen bottom reached
                if enemy_y1 > bottom:
                    self.clear_screen_objects()
                    messagebox.showerror(Consts.Enemy.screen_bottom_title,
                                         Consts.Enemy.screen_bottom_message)
                    return self.callback("same_level")

                if self.died(enemy):
                    self.enemies_list.remove(enemy)
                    self.canvas.delete(enemy.polygon)
                    sound.play_sound(Consts.Sound.exploded_file_name, 1)
            except Exception as exc_type:
                logging.exception(f"{type(exc_type).__name__}: {exc_type}")

        if len(self.enemies_list) == 0:
            self.clear_screen_objects()
            self.callback('next')

        self.root.after(Consts.Enemy.wait, lambda: self.move_enemy())


