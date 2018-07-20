import keyboard
import winsound
import threading
import time
from Logic import Logic
from tabulate import tabulate

dir_path = 'D:/osu!/Replays/*'  # 'E:/Games/osu!/Replays/*'
osu_api_key = '46de654115045a6e159919ebbc3f66a40fee404a'
profile_scores_count = 10
logic = Logic(dir_path, osu_api_key)
profiles = logic.get_profiles_sorted_by_total_pp()


def success_beep():
    frequency = 800
    duration = 250
    winsound.Beep(frequency, duration)


def failed_beep():
    frequency = 200
    duration = 250
    winsound.Beep(frequency, duration)


def submit_replay():
    result = logic.submit_replay()
    if result:
        success_beep()
        score, latest_pp, ranked_pp_obtained, total_pp_obtained = result
        display_score(score, latest_pp, ranked_pp_obtained, total_pp_obtained)
    else:
        failed_beep()
    update_profiles()
    print()
    display_profile_list()


def start_ui():
    global profiles
    program_running = True
    while program_running:
        update_profiles()
        display_profile_list()
        print("Choose profile: ", end="")
        print()
        choice = input()
        if choice.isnumeric() and 0 <= int(choice) < len(profiles):
            selected_profile = logic.get_or_create_profile(profiles[int(choice)].name)
        else:
            continue
        print()
        display_profile_details(selected_profile)
        print()


def display_profile_list():
    for i in range(len(profiles)):
        print(f"({i}): {profiles[i].name}, total pp: {round(profiles[i].total_pp)},"
              f" ranked pp: {round(profiles[i].ranked_pp)}")
    print()


def display_profile_details(profile):
    print(f"Profile Name: {profile.name}")
    print(f"Total PP: {round(profile.total_pp)}")
    print(f"Ranked PP: {round(profile.ranked_pp)}")
    print(f"Unranked PP: {round(profile.unranked_pp)}")
    print()
    headers = ["Title", "Acc", "Combo", "Miss", "Ranked", "PP"]
    score_rows = []

    scores = logic.get_scores_by_profile_id(profile.id)
    for score in scores:
        beatmap = logic.get_beatmap(score.beatmap_id)
        score_rows.append([f"{beatmap.title} [{beatmap.difficulty_name}]", round(score.accuracy, 2),
                           f"{score.max_combo}/{beatmap.max_combo}", score.misses, beatmap.is_ranked,
                           round(score.pp, 2)])
    print(tabulate(score_rows, headers=headers, tablefmt='orgtbl'))


def update_profiles():
    global profiles
    profiles = logic.get_profiles_sorted_by_total_pp()

def display_score(score, latest_pp, ranked_pp_obtained, total_pp_obtained):
    beatmap = logic.get_beatmap(score.beatmap_id)
    print(f"New {score.player_name} score: {beatmap.title} [{beatmap.difficulty_name}], pp: {round(latest_pp, 2)},"
          f" best pp: {round(score.pp, 2)} (total: + {round(total_pp_obtained, 2)}"
          f" , ranked: + {round(ranked_pp_obtained, 2)})) ")


keyboard.add_hotkey('ctrl+shift+f2', submit_replay)

print("PP Profile is running...")
print()

start_ui()


