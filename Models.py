class Profile:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.ranked_pp = 0
        self.unranked_pp = 0
        self.total_pp = 0
        self.rank = 0


class Beatmap:
    def __init__(self):
        self.id = 0
        self.creator = ''
        self.approach_rate = 0
        self.is_ranked = False
        self.circle_size = 0
        self.drain = 0
        self.beatmap_id = 0
        self.artist = ''
        self.overall_difficulty = 0
        self.total_length = 0
        self.title = ''
        self.bpm = 0
        self.stars = 0
        self.max_combo = 0
        self.hit_length = 0
        self.difficulty_name = ''


class Score:
    def __init__(self):
        self.id = 0
        self.beatmap_hash = ''
        self.player_name = ''
        self.number_300s = 0
        self.number_100s = 0
        self.number_50s = 0
        self.gekis = 0
        self.katus = 0
        self.misses = 0
        self.score = 0
        self.max_combo = 0
        self.is_perfect_combo = False
        self.no_fail = False
        self.easy = False
        self.hidden = False
        self.hard_rock = False
        self.sudden_death = False
        self.double_time = False
        self.relax = False
        self.half_time = False
        self.flashlight = False
        self.spun_out = False
        self.auto_pilot = False
        self.perfect = False
        self.pp = 0
        self.beatmap_id = 0
        self.profile_id = 0
        self.accuracy = 0

    def get_mods_string(self):
        mods = []
        if self.no_fail:
            mods.append("NF")
        if self.easy:
            mods.append("EZ")
        if self.hidden:
            mods.append("HD")
        if self.hard_rock:
            mods.append("HR")
        if self.sudden_death:
            mods.append("SD")
        if self.double_time:
            mods.append("DT")
        if self.relax:
            mods.append("RX")
        if self.half_time:
            mods.append("HT")
        if self.flashlight:
            mods.append("FL")
        if self.spun_out:
            mods.append("SO")
        if self.auto_pilot:
            mods.append("AP")
        if self.perfect:
            mods.append("PF")

        mods_string = ''.join(mods)

        return mods_string
