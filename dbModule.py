import pymysql
from collections import namedtuple


class Database():
    def __init__(self):
        self.db= pymysql.connect(host='127.0.0.1', port= 3306,
                                  user='root',
                                  password='input password!',
                                  db='epl',
                                  charset='utf8')
        self.cursor= self.db.cursor(pymysql.cursors.DictCursor)
        self.tcursor = self.db.cursor()

    def team_rank(self):
        team_for_rank = []
        self.cursor.execute("select teamname from Team")
        result = self.cursor.fetchall()
        team_list = []

        def cal_score(win, draw, lose) :
            return 3*win + 1*draw

        for row in result :
            team_list.append(row['teamname'])
        for team in team_list :
            sql = 'select * from Game where HomeTeam = %s OR AwayTeam = %s'
            self.cursor.execute(sql,(team, team))
            game_result = self.cursor.fetchall()
            win = 0
            draw = 0
            lose = 0
            for game in game_result :
                if game['HomeTeam'] == team :
                    if game['HomeScore'] > game['AwayScore'] :
                        win += 1
                    elif game['HomeScore'] == game['AwayScore'] :
                        draw += 1
                    else :
                        lose += 1
                else : 
                    if game['HomeScore'] < game['AwayScore'] :
                        win += 1
                    elif game['HomeScore'] == game['AwayScore'] :
                        draw += 1
                    else :
                        lose += 1
            res = {'name':team, 'win':win, 'draw':draw, 'lose':lose, 'score':cal_score(win,draw,lose)}
            team_for_rank.append(res)
        return sorted(team_for_rank, key=lambda x: x['score'], reverse= True) # 팀 랭킹 dict

    def temp_team(self) :
        self.cursor.execute("select teamname from Team")
        team = self.cursor.fetchall()
        return team

    def goal_rank(self) :
        sql = '''
        select concat(player.lastname,' ',player.firstname) as fullname, player.teamname as teamname, COUNT(*) AS totalgoal
        FROM Goal, player
        WHERE Goal.PlayerID = Player.PlayerID
        GROUP BY Goal.PlayerID
        ORDER BY TotalGoal DESC
        limit 10
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data # 골랭킹 제네레이터 dict

    def assist_rank(self) :
        sql = '''
        select concat(player.lastname,' ',player.firstname) as fullname, player.teamname as teamname, COUNT(*) AS totalassist
        FROM Goal, player
        WHERE Goal.AssistPlayerID = Player.PlayerID
        GROUP BY Goal.PlayerID
        ORDER BY totalassist DESC
        limit 10
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data # 어시랭킹 제네레이터 dict
        
    def game_list(self) :
        sql = '''
        select gameid, gamedate, round, hometeam, awayteam, homescore, awayscore, gamestadium as stadium
        FROM game''' 
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data #게임 아이디 포함해서 넘김 game 클릭시 반환

    def game_detail(self, gameid) :
        sql_home = '''
        select player.backnumber, concat(player.lastname,' ',player.firstname) as fullname, intime, 
        outtime, goal, assist, Yellowcard, Redcard, PerformanceRate
        from player, team_squad, game
        where game.gameid = {0} and team_squad.gameid= {0} and game.HomeTeam = team_squad.teamname
        and player.playerid= team_squad.playerid
        order by backnumber;
        '''.format(gameid)
        sql_away = '''
        select player.backnumber,concat(player.lastname,' ',player.firstname) as fullname, intime, 
        outtime, goal, assist, Yellowcard, Redcard, PerformanceRate
        from player, team_squad, game
        where game.gameid = {0} and team_squad.gameid= {0} and game.AwayTeam = team_squad.teamname
        and player.playerid= team_squad.playerid
        order by backnumber;
        '''.format(gameid)
        self.cursor.execute(sql_home)
        data_home = self.cursor.fetchall()
        self.cursor.execute(sql_away)
        data_away = self.cursor.fetchall()
        return data_home, data_away # 선수 이름 및 인타임 아웃타임 골 어시스트 .... 전부 반환

    def player_temp_list(self, name) :
        sql = 'select playerid, firstname, lastname, midname, teamname FROM player WHERE firstname=%s OR midname=%s OR lastname=%s'

        self.cursor.execute(sql,(name,name,name))
        data = self.cursor.fetchall()
        return data # Id 포함 모든 데이터 제네레이터

    def player_detail(self, playerid) :
        sql_game = '''
        select concat(player.lastname,' ',player.firstname) as fullname, teamname, dateofbirth, height, weight,
        position, preferredfoot, debutyear, nationality, contractdate, contractenddate, backnumber
        from player
        where playerid={}'''.format(playerid)
        self.cursor.execute(sql_game)
        data = self.cursor.fetchall()
        return data

    def team_detail(self, teamname) :
        sql_team = 'select * FROM Team WHERE TeamName = %s'
        self.cursor.execute(sql_team,(teamname))
        data_team = self.cursor.fetchall()
        sql_lastgame = '''
        select round, gamedate, hometeam, awayteam, homescore, awayscore
        FROM game
        where hometeam = %s OR awayteam =%s
        ORDER BY gamedate
        limit 5'''
        self.cursor.execute(sql_lastgame,(teamname,teamname))
        data_lastgame = self.cursor.fetchall()
        sql_teamplayer = '''
        select backnumber, concat(player.lastname,' ',player.firstname) as fullname, position
        FROM player
        where teamname = %s
        ORDER BY backnumber
        '''
        self.cursor.execute(sql_teamplayer, (teamname))
        data_teamplayer = self.cursor.fetchall()
        
        return data_team, data_lastgame, data_teamplayer

    def execute(self, query, args={}):
        self.cursor.execute(query, args) 
 
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchall()
        return row
    
    def texecute(self, query, args):
        self.tcursor.execute(query, args)
 
    def commit(self):
        self.db.commit()