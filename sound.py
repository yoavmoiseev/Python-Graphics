try:
    import winsound
    is_winsound = True
except ImportError:
    is_winsound = False  # TODO implement logic for Linux


def play_sound(sound, flags):
    if is_winsound:
        winsound.PlaySound(sound, flags)


def beep(frequency: int, duration: int):
    if is_winsound:
        winsound.Beep(frequency, duration)
