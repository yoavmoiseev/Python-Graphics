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
    default_game = "Clicker"
    all_colors = ["red", "green", "blue", "orange", "purple"]
    milliseconds = 0
    title = "Tkinter Games"
    window_state = "zoomed"
    close_window = "WM_DELETE_WINDOW"
    button_event_type = "<Enter>"
    choose_game_label = "Choose Game"
    first_game_name = "Clicker"
    second_game_name = "Catch the button"
    third_game_name = "Space Invaders"
    level_started_message = " level started"
    level_completed_message = " level successfully complete!"
    level_failed_message = " level failed!!! Starting same level again!"
    first_game_button_text = "Click me"
    second_game_button_text = "Catch Me"
    timer_label = "Timer"
    level_label = "Level-"
    timer_centering_parameter = 4
    timer_index = 3
    timer_wait = 100
    third_game_label = "Bullets-"
    third_game_index = 4
    button_beep_frequency = 1000
    button_beep_duration = 30


class Log:
    # logging messages
    unreachable = "Object is unreachable"
    file = 'TkinterGames.log'
    suffix = "-   successfully started"
    game_over = "The jet destroyed, the game is over!!!"
    win_info = "The -winfo_height()- fails, using -winfo_screenheight()- instead"
    window_destroyed = " window had been destroyed!"


class StarWars:
    key_event = "<KeyPress>"
    move_up_key = 'Up'
    move_down_key = 'Down'
    move_left_key = 'Left'
    move_right_key = 'Right'
    shoot_key = 'space'


class Sound:
    shoot_file_name = "sounds/shoot.wav"
    exploded_file_name = "sounds/enemy_exploded.wav"
    jet_injured_file_name = "sounds/jet-injured.wav"


class Others:
    screen_correction_y = 40
    fore_ground_color = "white"
