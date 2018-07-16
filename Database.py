import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('osu-pp-profile.db')
        self.c = self.conn.cursor()

        self.c.execute(''' create table if not exists beatmaps 
                       (id INTEGER PRIMARY KEY,
                       creator TEXT,
                       approach_rate REAL,
                       is_ranked INTEGER,
                       circle_size REAL,
                       drain REAL,
                       beatmap_id INTEGER,
                       artist TEXT,
                       overall_difficulty REAL,
                       total_length REAL,
                       title TEXT,
                       bpm REAL,
                       stars REAL,
                       max_combo INTEGER,
                       hit_length REAL,
                       difficulty_name TEXT) ''')

        self.c.execute(''' create table if not exists profiles 
                       (id INTEGER PRIMARY KEY,
                       name TEXT,
                       ranked_pp REAL,
                       unranked_pp REAL,
                       total_pp REAL,
                       rank INTEGER) ''')

        self.c.execute(''' create table if not exists scores 
                       (id INTEGER PRIMARY KEY,
                       beatmap_hash TEXT,
                       player_name TEXT,
                       number_300s INTEGER,
                       number_100s INTEGER,
                       number_50s INTEGER,
                       gekis INTEGER,
                       katus INTEGER,
                       misses INTEGER,
                       score INTEGER,
                       max_combo INTEGER,
                       is_perfect_combo INTEGER,
                       no_fail INTEGER,
                       easy INTEGER,
                       hidden INTEGER,
                       hard_rock INTEGER,
                       sudden_death INTEGER,
                       double_time INTEGER,
                       relax INTEGER,
                       half_time INTEGER,
                       flashlight INTEGER,
                       spun_out INTEGER,
                       auto_pilot INTEGER,
                       perfect INTEGER,
                       beatmap_id INTEGER,
                       profile_id INTEGER,
                       FOREIGN KEY(beatmap_id) REFERENCES beatmaps(id),
                       FOREIGN KEY(profile_id) REFERENCES profiles(id)) ''')

    def get_all_scores(self):
        result = self.c.execute('select * from scores').fetchall()
        return result
