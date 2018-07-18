import sqlite3
from Models import Score, Beatmap, Profile

class Database:
    def __init__(self, database_file_name):
        self.database_file_name = database_file_name
        self.conn = sqlite3.connect(self.database_file_name)
        self.c = self.conn.cursor()

        self.c.execute(''' 
            CREATE TABLE IF NOT EXISTS beatmaps (
                id INTEGER PRIMARY KEY,
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
                difficulty_name TEXT
            )
        ''')

        self.c.execute(''' 
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY,
                name TEXT,
                ranked_pp REAL,
                unranked_pp REAL,
                total_pp REAL,
                rank INTEGER 
            )
        ''')

        self.c.execute(''' 
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY,
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
                pp REAL,
                beatmap_id INTEGER,
                profile_id INTEGER,
                accuracy REAL,
                FOREIGN KEY(beatmap_id) REFERENCES beatmaps(id),
                FOREIGN KEY(profile_id) REFERENCES profiles(id)
            )
        ''')

        self.conn.close()

    def map_beatmap_query_result(self, query_result):
        beatmaps = []
        for row in query_result:
            beatmap = Beatmap()

            beatmap.id = int(row[0])
            beatmap.creator = row[1]
            beatmap.approach_rate = float(row[2])
            beatmap.is_ranked = bool(row[3])
            beatmap.circle_size = float(row[4])
            beatmap.drain = float(row[5])
            beatmap.beatmap_id = int(row[6])
            beatmap.artist = row[7]
            beatmap.overall_difficulty = float(row[8])
            beatmap.total_length = float(row[9])
            beatmap.title = row[10]
            beatmap.bpm = float(row[11])
            beatmap.stars = float(row[12])
            beatmap.max_combo = int(row[13])
            beatmap.hit_length = float(row[14])
            beatmap.difficulty_name = row[15]

            beatmaps.append(beatmap)

        return beatmaps

    def get_beatmap_by_beatmap_id(self, beatmap_id):
        self.conn = sqlite3.connect(self.database_file_name)
        self.c = self.conn.cursor()
        self.c.execute('select * from beatmaps where beatmap_id = {0}'.format(beatmap_id))
        query_result = self.c.fetchall()
        beatmaps = self.map_beatmap_query_result(query_result)
        self.conn.close()
        if beatmaps:
            return beatmaps[0]
        return beatmaps

    def get_beatmap_by_id(self, id):
        self.conn = sqlite3.connect(self.database_file_name)
        self.c = self.conn.cursor()
        self.c.execute('select * from beatmaps where id = {0}'.format(id))
        query_result = self.c.fetchall()
        beatmaps = self.map_beatmap_query_result(query_result)
        self.conn.close()
        if beatmaps:
            return beatmaps[0]
        return beatmaps

    def create_beatmap(self, beatmap_model):
        self.conn = sqlite3.connect(self.database_file_name)
        self.c = self.conn.cursor()
        sql = ''' 
            INSERT INTO beatmaps(creator,approach_rate,is_ranked,circle_size,drain,beatmap_id,artist,overall_difficulty,
                total_length,title,bpm,stars,max_combo,hit_length,difficulty_name)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''

        self.c.execute(sql, (beatmap_model.creator, beatmap_model.approach_rate, beatmap_model.is_ranked,
                             beatmap_model.circle_size, beatmap_model.drain, beatmap_model.beatmap_id,
                             beatmap_model.artist, beatmap_model.overall_difficulty,
                             beatmap_model.total_length, beatmap_model.title, beatmap_model.bpm, beatmap_model.stars,
                             beatmap_model.max_combo, beatmap_model.hit_length, beatmap_model.difficulty_name))

        self.conn.commit()
        result = self.c.lastrowid
        self.conn.close()
        return result


    def map_profile_query_result(self, query_result):
        profiles = []
        for row in query_result:
            profile = Profile()

            profile.id = int(row[0])
            profile.name = row[1]
            profile.ranked_pp = float(row[2])
            profile.unranked_pp = float(row[3])
            profile.total_pp = float(row[4])
            profile.rank = int(row[5])

            profiles.append(profile)

        return profiles

    def get_profile_by_name(self, name):
        self.conn = sqlite3.connect(self.database_file_name)
        self.c = self.conn.cursor()
        self.c.execute("select * from profiles where name = '{0}'".format(name))
        query_result = self.c.fetchall()
        profiles = self.map_profile_query_result(query_result)
        self.conn.close()
        if profiles:
            return profiles[0]
        return profiles

    def get_profile_by_id(self, id):
        self.conn = sqlite3.connect(self.database_file_name)
        self.c = self.conn.cursor()
        self.c.execute("select * from profiles where id = {0}".format(id))
        query_result = self.c.fetchall()
        profiles = self.map_profile_query_result(query_result)
        self.conn.close()
        if profiles:
            return profiles[0]
        return profiles

    def create_profile(self, profile_model):
        self.conn = sqlite3.connect(self.database_file_name)
        self.c = self.conn.cursor()

        sql = ''' 
            INSERT INTO profiles(name,ranked_pp,unranked_pp,total_pp,rank)
            VALUES(?,?,?,?,?)
        '''
        self.c.execute(sql, (profile_model.name, profile_model.ranked_pp, profile_model.unranked_pp,
                             profile_model.total_pp, profile_model.rank))

        self.conn.commit()
        result = self.c.lastrowid
        self.conn.close()
        return result

    def map_score_query_result(self, query_result):
        scores = []
        for row in query_result:
            score = Score()

            score.id = int(row[0])
            score.beatmap_hash = row[1]
            score.player_name = row[2]
            score.number_300s = int(row[3])
            score.number_100s = int(row[4])
            score.number_50s = int(row[5])
            score.gekis = int(row[6])
            score.katus = int(row[7])
            score.misses = int(row[8])
            score.score = int(row[9])
            score.max_combo = int(row[10])
            score.is_perfect_combo = bool(row[11])
            score.no_fail = bool(row[12])
            score.easy = bool(row[13])
            score.hidden = bool(row[14])
            score.hard_rock = bool(row[15])
            score.sudden_death = bool(row[16])
            score.double_time = bool(row[17])
            score.relax = bool(row[18])
            score.half_time = bool(row[19])
            score.flashlight = bool(row[20])
            score.spun_out = bool(row[21])
            score.auto_pilot = bool(row[22])
            score.perfect = bool(row[23])
            score.pp = float(row[24])
            score.beatmap_id = int(row[25])
            score.profile_id = int(row[26])
            score.accuracy = float(row[27])

            scores.append(score)

        return scores

    def get_score_by_beatmap_id_and_profile_id(self, beatmap_id, profile_id):
        self.conn = sqlite3.connect(self.database_file_name)
        self.c = self.conn.cursor()
        self.c.execute("select * from scores where beatmap_id = {0} and profile_id = {1}".format(beatmap_id, profile_id))
        query_result = self.c.fetchall()
        scores = self.map_score_query_result(query_result)
        self.conn.close()
        if scores:
            return scores[0]
        return scores

    def get_score_by_id(self, id):
        self.conn = sqlite3.connect(self.database_file_name)
        self.c = self.conn.cursor()
        self.c.execute("select * from scores where id = {0}".format(id))
        query_result = self.c.fetchall()
        scores = self.map_score_query_result(query_result)
        self.conn.close()
        if scores:
            return scores[0]
        return scores

    def create_score(self, score_model):
        self.conn = sqlite3.connect(self.database_file_name)
        self.c = self.conn.cursor()

        sql = ''' 
            INSERT INTO scores(beatmap_hash,player_name,number_300s,number_100s,number_50s,gekis,katus,misses,score,
                max_combo,is_perfect_combo,no_fail,easy,hidden,hard_rock,sudden_death,double_time,relax,half_time,
                flashlight,spun_out,auto_pilot,perfect,pp,beatmap_id,profile_id,accuracy)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        self.c.execute(sql, (score_model.beatmap_hash, score_model.player_name, score_model.number_300s,
                             score_model.number_100s, score_model.number_50s, score_model.gekis, score_model.katus,
                             score_model.misses, score_model.score, score_model.max_combo, score_model.is_perfect_combo,
                             score_model.no_fail, score_model.easy, score_model.hidden, score_model.hard_rock,
                             score_model.sudden_death, score_model.double_time, score_model.relax,
                             score_model.half_time, score_model.flashlight, score_model.spun_out,
                             score_model.auto_pilot, score_model.perfect, score_model.pp, score_model.beatmap_id,
                             score_model.profile_id, score_model.accuracy))

        self.conn.commit()
        result = self.c.lastrowid
        self.conn.close()
        return result

    def update_score(self, score_model):
        self.conn = sqlite3.connect(self.database_file_name)
        self.c = self.conn.cursor()
        
        sql = '''UPDATE scores SET beatmap_hash = ?, player_name = ?, number_300s = ?, number_100s = ?, number_50s = ?,
            gekis = ?, katus = ?, misses = ?, score = ?, max_combo = ?, is_perfect_combo = ?, no_fail = ?, easy = ?,
            hidden = ?, hard_rock = ?, sudden_death = ?, double_time = ?, relax = ?, half_time = ?, flashlight = ?, 
            spun_out = ?, auto_pilot = ?, perfect = ?, pp = ?, beatmap_id = ?, profile_id = ?, accuracy = ?
            WHERE id = ? '''

        self.c.execute(sql, (score_model.beatmap_hash, score_model.player_name, score_model.number_300s,
                             score_model.number_100s, score_model.number_50s, score_model.gekis, score_model.katus,
                             score_model.misses, score_model.score, score_model.max_combo, score_model.is_perfect_combo,
                             score_model.no_fail, score_model.easy, score_model.hidden, score_model.hard_rock,
                             score_model.sudden_death, score_model.double_time, score_model.relax,
                             score_model.half_time, score_model.flashlight, score_model.spun_out,
                             score_model.auto_pilot, score_model.perfect, score_model.pp, score_model.beatmap_id,
                             score_model.profile_id, score_model.accuracy, score_model.id))

        self.conn.commit()
        result = self.c.lastrowid
        self.conn.close()
        return result