import tkinter
from random import randrange

import sound
import consts
from StarWars import *


class TkinterGames:
    """
    Creates a graphic window with a menu for selecting games
    """

    def __init__(self, game_selected=consts.TkinterGames.default_game):
        """
        constructor, builds the main window with the menus and "Click Me" button
        """
        logging.info(game_selected + consts.Log.suffix)

        self.selected_game = game_selected
        self.color_index = 0
        self.all_colors = consts.TkinterGames.all_colors
        self.milliseconds = consts.TkinterGames.milliseconds

        self.root = tk.Tk()
        self.root.title(game_selected)
        try:
            self.root.wm_state(consts.TkinterGames.window_state)
        except tkinter.TclError:  # we are not in windows
            self.root.attributes('-zoomed', True)

        # menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.choose_game_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=consts.TkinterGames.choose_game_label,
                                  menu=self.choose_game_menu)
        self.add_choices_to_menu()

        # shifting the stopper to the middle
        shift = self.root.winfo_screenheight() // consts.TkinterGames.timer_centering_parameter
        self.menu_bar.add_command(label=' ' * shift, state=tk.DISABLED)

        self.menu_bar.add_command(label=consts.TkinterGames.timer_label, state=tk.DISABLED)

        self.stop_watch()

        self.catch_me_button = ...,

        self.root.protocol(consts.TkinterGames.close_window, self.close_main_window)

        # Star Wars game started
        if self.selected_game == consts.TkinterGames.third_game_name:
            self.menu_bar.add_command(label=consts.TkinterGames.third_game_label + str(consts.Bullet.max), state=tk.DISABLED)
            StarWars(self.root, self.menu_bar)
        else:
            self.create_catch_me_button()
            self.catch_me_button.bind(consts.TkinterGames.button_event_type, self.on_mouse_on)

        # Only commands up here will be displayed/executed
        self.root.mainloop()

    def close_main_window(self):
        logging.info(consts.TkinterGames.title + consts.Log.window_destroyed)
        self.menu_bar.after_cancel(self.after_id)
        self.root.destroy()  # Close the window

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

        self.menu_bar.entryconfig(consts.TkinterGames.timer_index, label=stopper_str)
        self.after_id = self.menu_bar.after(consts.TkinterGames.timer_wait, self.stop_watch)

    def create_catch_me_button(self):
        button_text = ""
        # Create a button with text according to menu selected
        # and place it in the window
        if self.selected_game == consts.TkinterGames.first_game_name:
            button_text = consts.TkinterGames.first_game_button_text
        elif self.selected_game == consts.TkinterGames.second_game_name:
            button_text = consts.TkinterGames.second_game_button_text

        self.catch_me_button = tk.Button(self.root, text=button_text,
                                         command=self.on_button_click)
        self.catch_me_button.pack(pady=20)

    # Function to be called when the button is clicked
    def on_button_click(self):
        self.color_index += 1
        self.catch_me_button.config(bg=self.all_colors[self.color_index % len(self.all_colors)],
                                    fg=consts.Others.fore_ground_color,
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
        if self.selected_game != consts.TkinterGames.second_game_name:
            return

        self.color_index += 1
        self.catch_me_button.config(bg=self.all_colors[self.color_index % len(self.all_colors)],
                                    fg=consts.Others.fore_ground_color, text=str(self.color_index))

        self.catch_me_button.place(x=randrange(self.root.winfo_width() - self.catch_me_button.winfo_width()),
                                   y=randrange(self.root.winfo_height()) - self.catch_me_button.winfo_height())
        sound.beep(consts.TkinterGames.button_beep_frequency, consts.TkinterGames.button_beep_duration)

    # Function to be called when a menu item is selected
    def menu_choice(self, choice):
        logging.info(self.root.title() + consts.Log.window_destroyed)
        self.close_main_window()
        logging.info("This is the choice %s", choice)
        self.__init__(choice)

    def reset_timer(self):
        self.milliseconds = 0

    def add_choices_to_menu(self):
        game_names = [consts.TkinterGames.first_game_name,
                      consts.TkinterGames.second_game_name,
                      consts.TkinterGames.third_game_name]

        def make_menu_command(cmd):
            return lambda: self.menu_choice(cmd)

        for game_name in game_names:
            self.choose_game_menu.add_command(
                label=game_name, command=make_menu_command(game_name))
        self.choose_game_menu.add_separator()  # Add a separator line


if __name__ == "__main__":
    logging.basicConfig(filename=consts.Log.file, level=logging.DEBUG,
                        format='%(levelname)s - %(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    create_window = TkinterGames()
