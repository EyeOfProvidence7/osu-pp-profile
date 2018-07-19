import keyboard
import winsound
from Logic import Logic

dir_path = 'E:/Games/osu!/Replays/*'  # 'D:/osu!/Replays/*'
osu_api_key = '46de654115045a6e159919ebbc3f66a40fee404a'

logic = Logic(dir_path, osu_api_key)


def success_beep():
    frequency = 800
    duration = 250
    winsound.Beep(frequency, duration)


def failed_beep():
    frequency = 200
    duration = 250
    winsound.Beep(frequency, duration)


def submit_replay():
    success = logic.submit_replay()
    if success:
        success_beep()
    else:
        failed_beep()


keyboard.add_hotkey('ctrl+shift+f2', submit_replay)

print("PP Profile is running...")
input()
