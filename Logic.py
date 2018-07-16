import keyboard
import time
import os
import glob
import winsound
import requests
from Models import Score, Beatmap
from Database import Database
from osrparse import parse_replay_file
from osrparse.enums import Mod, GameMode

dir_path = 'E:/Games/osu!/Replays/*'
replay_wait_period = 100
replay_wait_timeout = 5000
submit_replay_lock = False
osu_api_key = '50a9e71fb7203e281868a35e1f45e4236d62a7d1'
database = Database()


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
    list_of_files = glob.glob(dir_path)
    latest_file = max(list_of_files, key=os.path.getmtime)
    latest_file_time = int(round(os.path.getmtime(latest_file) * 1000))
    replay = get_early_replay(latest_file, latest_file_time)
    if replay is None:
        replay = get_late_replay(latest_file_time)

    return replay


def submit_replay():
    global submit_replay_lock
    if submit_replay_lock:
        return
        submit_replay_lock = True

    replay_to_submit = get_replay()
    if replay_to_submit is None:
        failed_beep()
        print("Failed to find replay.")

    try:
        score_model = create_score_model(replay_to_submit)
    except Exception as e:
        failed_beep()
        print("Failed to create score model. Exception: {0}".format(e))
        return

    success_beep()
    submit_replay_lock = False
    

def map_score_model(replay):
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


def map_beatmap_model(beatmap):
    beatmap_model = Beatmap()

    beatmap_model.creator = beatmap['creator']
    beatmap_model.approach_rate = float(beatmap['diff_approach'])
    beatmap_model.is_ranked = beatmap['approved'] == 1
    beatmap_model.circle_size = float(beatmap['diff_size'])
    beatmap_model.drain = float(beatmap['diff_drain'])
    beatmap_model.beatmap_id = int(beatmap['beatmap_id'])
    beatmap_model.artist = beatmap['artist']
    beatmap_model.overall_difficulty = float(beatmap['diff_overall'])
    beatmap_model.total_length = float(beatmap['total_length'])
    beatmap_model.title = beatmap['title']
    beatmap_model.bpm = float(beatmap['bpm'])
    beatmap_model.stars = float(beatmap['difficultyrating'])
    beatmap_model.max_combo = int(beatmap['max_combo'])
    beatmap_model.hit_length = float(beatmap['hit_length'])
    beatmap_model.difficulty_name = beatmap['version']

    return beatmap_model


def create_beatmap_model(beatmap_hash):
    beatmap_url = "https://osu.ppy.sh/api/get_beatmaps?k={0}&h={1}".format(osu_api_key, beatmap_hash)
    r = requests.get(beatmap_url)
    if not r.json():
        raise Exception("Beatmap not found.");

    beatmap_json = r.json()[0]
    beatmap_model = map_beatmap_model(beatmap_json)

    return beatmap_model


def create_score_model(replay):
    parsed_replay = parse_replay_file(replay)
    if parsed_replay.game_mode != GameMode.Standard:
        raise Exception('Only osu!standard game mode is supported.')

    beatmap_model = create_beatmap_model(parsed_replay.beatmap_hash)

    score_model = map_score_model(parsed_replay)
    print(score_model)

    return score_model


keyboard.add_hotkey('ctrl+f2', submit_replay)

print("PP Profile is running...")
input()
