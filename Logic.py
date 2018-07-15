import keyboard
import time
import os
import glob
import winsound
from Models import Score
from osrparse import parse_replay_file
from osrparse.enums import Mod, GameMode

dir_path = 'D:/osu!/Replays/*'
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


def get_early_replay(latest_file, latest_file_time):
    replay_to_submit = None
    current_time = int(round(time.time() * 1000))
    earliest_replay_time = current_time - replay_wait_timeout
    if earliest_replay_time <= latest_file_time <= current_time:
        replay_to_submit = latest_file

    return replay_to_submit


def get_late_replay(latest_file_time):
    replay_to_submit = None
    replay_wait_time = 0
    while replay_wait_time < replay_wait_timeout:
        time.sleep(replay_wait_period / 1000.0)
        replay_wait_time += replay_wait_period
        list_of_files = glob.glob(dir_path)
        latest_file = max(list_of_files, key=os.path.getmtime)
        new_latest_file_time = int(round(os.path.getmtime(latest_file) * 1000))
        if new_latest_file_time != latest_file_time:
            replay_to_submit = latest_file
            break

    return replay_to_submit


def get_replay():
    global get_replay_lock
    if get_replay_lock:
        return
    get_replay_lock = True
    list_of_files = glob.glob(dir_path)
    latest_file = max(list_of_files, key=os.path.getmtime)
    latest_file_time = int(round(os.path.getmtime(latest_file) * 1000))
    replay_to_submit = get_early_replay(latest_file, latest_file_time)
    if replay_to_submit is None:
        replay_to_submit = get_late_replay(latest_file_time)

    if replay_to_submit is not None:
        submit_replay(replay_to_submit)
    else:
        failed_beep()
        print("Failed to find replay :(")
        
    get_replay_lock = False
    

def create_score_model(replay):
    score_model = Score()
    
    score_model.beatmap_hash = replay.beatmap_hash
    score_model.player_name = replay.player_name
    score_model.number_300s = replay.number_300s
    score_model.number_100s = replay.number_100s
    score_model.number_50s = replay.number_50s
    score_model.gekis = replay.gekis
    score_model.katus = replay.katus
    score_model.misses = replay.misses
    score_model.score = replay.score
    score_model.max_combo = replay.max_combo
    score_model.is_perfect_combo = replay.is_perfect_combo

    score_model.no_fail = Mod.NoFail in replay.mod_combination
    score_model.easy = Mod.Easy in replay.mod_combination
    score_model.hidden = Mod.Hidden in replay.mod_combination
    score_model.hard_rock = Mod.HardRock in replay.mod_combination
    score_model.sudden_death = Mod.SuddenDeath in replay.mod_combination
    score_model.double_time = Mod.DoubleTime in replay.mod_combination or Mod.Nightcore in replay.mod_combination
    score_model.relax = Mod.Relax in replay.mod_combination
    score_model.half_time = Mod.HalfTime in replay.mod_combination
    score_model.flashlight = Mod.Flashlight in replay.mod_combination
    score_model.spun_out = Mod.SpunOut in replay.mod_combination
    score_model.auto_pilot = Mod.Autopilot in replay.mod_combination
    score_model.perfect = Mod.Perfect in replay.mod_combination

    return score_model


def submit_replay(replay):
    parsed_replay = None
    try:
        parsed_replay = parse_replay_file(replay)
    except:
        failed_beep()
        print("Replay data is corrupt")
        return
    if parsed_replay.game_mode != GameMode.Standard:
        failed_beep()
        print("Wrong game mode :(")
        return
    score_model = create_score_model(parsed_replay)
    print(score_model)
    success_beep()


keyboard.add_hotkey('ctrl+f2', get_replay)

input()
