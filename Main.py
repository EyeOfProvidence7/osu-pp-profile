import keyboard
import winsound
from Logic import Logic
from tabulate import tabulate

dir_path = 'D:/osu!/Replays/*'  # 'E:/Games/osu!/Replays/*'
osu_api_key = '46de654115045a6e159919ebbc3f66a40fee404a'
profile_scores_count = 10

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


def start_ui():
    program_running = True
    while program_running:
        profiles = logic.get_profiles_sorted_by_total_pp()
        display_profile_list(profiles)
        print("Choose profile: ", end="")
        print()
        choice = int(input())
        selected_profile = logic.get_or_create_profile(profiles[choice].name)
        print()
        display_profile_details(selected_profile)
        print()


def display_profile_list(profiles):
    for i in range(len(profiles)):
        print(f"({i}): {profiles[i].name}, total pp: {round(profiles[i].total_pp)}")
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
        score_rows.append([f"{beatmap.title} [{beatmap.difficulty_name}]", score.accuracy,
                           f"{score.max_combo}/{beatmap.max_combo}", score.misses, beatmap.is_ranked, score.pp])
    print(tabulate(score_rows, headers=headers, tablefmt='orgtbl'))


keyboard.add_hotkey('ctrl+shift+f2', submit_replay)

print("PP Profile is running...")
print()
start_ui()
