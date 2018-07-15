import keyboard
import time
import os
import glob
import winsound

dir_path = 'E:/Games/osu!/Replays/*'
replay_wait_period = 100
replay_wait_timeout = 5000
get_replay_lock = False


def success_beep():
    frequency = 800  # Set Frequency To 2500 Hertz
    duration = 250  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)


def failed_beep():
    frequency = 200  # Set Frequency To 2500 Hertz
    duration = 250  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)


def get_early_replay(latest_file):
    replay_to_submit = None
    current_time = int(round(time.time() * 1000))
    latest_file_time = int(round(os.path.getmtime(latest_file) * 1000))
    earliest_replay_time = current_time - replay_wait_timeout
    if earliest_replay_time <= latest_file_time <= current_time:
        replay_to_submit = latest_file

    return replay_to_submit


def get_late_replay(latest_file):
    replay_to_submit = None
    replay_wait_time = 0
    while replay_wait_time < replay_wait_timeout:
        time.sleep(replay_wait_period / 1000.0)
        replay_wait_time += replay_wait_period
        list_of_files = glob.glob(dir_path)
        latest_file_2 = max(list_of_files, key=os.path.getmtime)
        if os.path.getmtime(latest_file_2) != os.path.getmtime(latest_file):
            replay_to_submit = latest_file_2
            break

    return replay_to_submit


def get_replay():
    global get_replay_lock
    if get_replay_lock:
        return
    get_replay_lock = True
    list_of_files = glob.glob(dir_path)
    latest_file = max(list_of_files, key=os.path.getmtime)
    replay_to_submit = get_early_replay(latest_file)
    if replay_to_submit is None:
        replay_to_submit = get_late_replay(latest_file)

    if replay_to_submit is not None:
        success_beep()
        submit_replay(replay_to_submit)
    else:
        failed_beep()
        print("Failed to find replay :(")

    get_replay_lock = False


def submit_replay(replay):
    print(replay)


keyboard.add_hotkey('ctrl+f2', get_replay)

input()
