import keyboard
import time
import os
import glob
import winsound
import requests
import traceback
import sys
import pyttanko as osu
import codecs
from pprint import pprint
from Models import Score, Beatmap, Profile
from Database import Database
from osrparse import parse_replay_file
from osrparse.enums import Mod, GameMode

dir_path = 'D:/osu!/Replays/*'  # 'E:/Games/osu!/Replays/*'
replay_wait_period = 100
replay_wait_timeout = 5000
submit_replay_lock = False
osu_api_key = '46de654115045a6e159919ebbc3f66a40fee404a'
temp_beatmap_name = "workaround.osu"
database_file_name = 'osu-pp-profile.db'
database = Database(database_file_name)


def success_beep():
    frequency = 800
    duration = 250
    winsound.Beep(frequency, duration)


def failed_beep():
    frequency = 200
    duration = 250
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

    try:
        replay_to_submit = get_replay()
    except PermissionError:
        time.sleep(1)
        replay_to_submit = get_replay()

    if replay_to_submit is None:
        failed_beep()
        print("Failed to find replay.")
        return

    try:
        parsed_replay = parse_replay_file(replay_to_submit)
    except PermissionError:
        time.sleep(1)
        parsed_replay = parse_replay_file(replay_to_submit)
    except:
        failed_beep()
        traceback.print_exc(file=sys.stdout)
        return

    try:
        if parsed_replay.game_mode != GameMode.Standard:
            raise Exception('Only osu!standard game mode is supported.')
        beatmap = get_or_create_beatmap(parsed_replay.beatmap_hash)
        profile = get_or_create_profile(parsed_replay.player_name)
        score = get_or_create_or_update_score(parsed_replay, beatmap, profile)
        pprint(vars(score))
        # ToDo: update_profile(profile)
    except:
        failed_beep()
        traceback.print_exc(file=sys.stdout)
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
    beatmap_model.is_ranked = beatmap['approved'] == '1'
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


def get_or_create_beatmap(beatmap_hash):
    beatmap_url = "https://osu.ppy.sh/api/get_beatmaps?k={0}&h={1}".format(osu_api_key, beatmap_hash)
    r = requests.get(beatmap_url)
    if not r.json():
        raise Exception("Beatmap not found.");

    beatmap_json = r.json()[0]
    beatmap_model = map_beatmap_model(beatmap_json)
    beatmap_entity = database.get_beatmap_by_beatmap_id(beatmap_model.beatmap_id)
    if not beatmap_entity:
        beatmap_entity_id = database.create_beatmap(beatmap_model)
        beatmap_entity = database.get_beatmap_by_id(beatmap_entity_id)

    return beatmap_entity


def get_or_create_profile(profile_name):
    profile_model = Profile()
    profile_model.name = profile_name

    profile_entity = database.get_profile_by_name(profile_model.name)
    if not profile_entity:
        profile_entity_id = database.create_profile(profile_model)
        profile_entity = database.get_profile_by_id(profile_entity_id)

    return profile_entity


def get_or_create_or_update_score(replay, beatmap, profile):
    score_model = map_score_model(replay)
    score_model.beatmap_id = beatmap.id
    score_model.profile_id = profile.id
    score_model.pp, score_model.accuracy = calculate_score_pp(beatmap.beatmap_id, score_model)

    score_entity = database.get_score_by_beatmap_id_and_profile_id(beatmap.id, profile.id)

    if not score_entity:
        score_entity_id = database.create_score(score_model)
        score_entity = database.get_score_by_id(score_entity_id)
    elif score_entity.pp < score_model.pp:
        score_model.id = score_entity.id
        database.update_score(score_model)
        score_entity = score_model

    return score_entity


def calculate_score_pp(beatmap_id, score):
    p = osu.parser()
    beatmap_url = "https://osu.ppy.sh/osu/{0}".format(beatmap_id)
    beatmap_raw = requests.get(beatmap_url).text
    f = codecs.open(temp_beatmap_name, "w+", "utf-8")
    f.write(beatmap_raw)
    f.close()
    f = codecs.open(temp_beatmap_name, encoding="utf-8")
    clean_beatmap = p.map(f)
    f.close()
    os.remove(temp_beatmap_name)

    stars = osu.diff_calc().calc(clean_beatmap, osu.mods_from_str(score.get_mods_string()))

    pp, _, _, _, acc = osu.ppv2(aim_stars=stars.aim, speed_stars=stars.speed, bmap=clean_beatmap,
                                mods=osu.mods_from_str(score.get_mods_string()), combo=score.max_combo,
                                n300=score.number_300s, n100=score.number_100s, n50=score.number_50s,
                                nmiss=score.misses)
    return pp, acc


keyboard.add_hotkey('ctrl+f2', submit_replay)

print("PP Profile is running...")
input()
