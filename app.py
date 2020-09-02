# -*- coding: utf-8 -*-
import datetime
import tkinter as tk
from tkinter import ttk, filedialog
from dbModule import Database
from collections import namedtuple


class Counter_program():

    def __init__(self, db):
        self.window = tk.Tk()
        self.window.title("EPL")
        self.window.geometry("1000x500+100+100")
        self.create_mainwidgets()

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.db = db

    def create_mainwidgets(self):
        # Create some room around all the internal frames
        self.window['padx'] = 5
        self.window['pady'] = 5

        # - - - - - - - - - - - - - - - - - - - - -
        # The rank frame
        self.rank_frame = ttk.LabelFrame(self.window, text="Rank Info", relief=tk.RIDGE)
        self.rank_frame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        rank_btn = ttk.Button(self.rank_frame, text="Ranking", command=self.rank_widget)
        rank_btn.pack(side='top', fill='both')

        # - - - - - - - - - - - - - - - - - - - - -
        # The game frame
        self.game_frame = ttk.LabelFrame(self.window, text="Game Info", relief=tk.RIDGE)
        self.game_frame.grid(row=0, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=6)

        game_btn = ttk.Button(self.game_frame, text="Game", command=self.game_list_widget)
        game_btn.pack(side='top', fill='both')

        # - - - - - - - - - - - - - - - - - - - - -
        # The team list frame
        self.team_frame = ttk.LabelFrame(self.window, text="Team", relief=tk.RIDGE)
        self.team_frame.grid(row=1, column=0, rowspan=2, sticky=tk.E + tk.W + tk.N + tk.S)

        team_tree=ttk.Treeview(self.team_frame, columns=["Team",])        
        team_tree.pack(side='top', fill='both')
        
        team_tree.column("#0", width=50)
        team_tree.heading("#0", text="num")
        
        team_tree.column("Team", width=150, anchor="w")
        team_tree.heading("Team", text="team", anchor="center")

        for no, row in enumerate(db.temp_team()) :
            team_tree.insert('', 'end', text=str(no+1), values=[row[i] for i in ('teamname',)])
        
        def team_select(event):
            team = team_tree.item(event.widget.selection())['values'][0]
            return self.team_list_window(team)
        
        team_tree.bind('<<TreeviewSelect>>', team_select)

        # The Player Search frame
        self.player_frame = ttk.LabelFrame(self.window, text="Player", relief=tk.RIDGE)
        self.player_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S)
        self.player_frame.grid_columnconfigure(0, weight=7)
        self.player_frame.grid_columnconfigure(1, weight=3)
        self.player_frame.grid_rowconfigure(0, weight=1)
        self.player_frame.grid_rowconfigure(1, weight=9)
        
        self.player_search = ttk.Entry(self.player_frame)
        self.player_search.grid(row = 0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        def search() :
            a = self.player_search.get()
            res = db.player_temp_list(a)
            return self.make_temp_list(res)

        self.player_search_btn = ttk.Button(self.player_frame, text='search', command=search)
        self.player_search_btn.grid(row=0, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        # ----------
        # admin btn
        def admin_start() :
            admin = AdminMode(self.db)

        self.admin_frame = ttk.LabelFrame(self.window, text="Update match", relief=tk.RIDGE)
        self.admin_frame.grid(row=2, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        rank_btn = ttk.Button(self.admin_frame, text="update", command=admin_start)
        rank_btn.pack(side='top', fill='both')

    def make_temp_list(self, data) : 
        self.playerview=ttk.Treeview(self.player_frame)
        col = ('playerid',"firstname","lastname", "midname", 'teamname')
        self.playerview['columns'] = col         
        self.playerview['displaycolumns'] = col[1:]         
        self.playerview.grid(row=1,column=0, columnspan=2, sticky=tk.E + tk.W + tk.N + tk.S)

        self.playerview.column("#0", width=50, stretch=tk.NO)
        for i in col :
            self.playerview.column(i, width=100)

        self.playerview.heading("#0",text="#",anchor='center')
        for i in col :
            self.playerview.heading(i, text=i, anchor='center')

        for rank, row in enumerate(data) :
            self.playerview.insert('', 'end', text=str(rank+1), values=[row[i] for i in col])

        def player_select(event):
            playerid = self.playerview.item(event.widget.selection())['values'][0]
            print(playerid)
            return self.player_detail_widget(playerid)

        self.playerview.bind('<<TreeviewSelect>>', player_select)

    # player detail widget
    def player_detail_widget(self, playerid) :
        window = tk.Tk()
        data = db.player_detail(playerid)
        window.title(data[0]['fullname'])
        window.geometry("1200x400+100+100")
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=5)
        style = ttk.Style(window)
        style.configure('Treeview', rowheight=50)

        label=tk.Label(window, text='ALL ABOUT {}'.format(data[0]['fullname']), width=50, height=10)
        label.grid(row=0, column=0)
        
        window['padx'] = 5
        window['pady'] = 5
     
        frame = ttk.LabelFrame(window, text=data[0]['fullname'], relief=tk.RIDGE)
        frame.grid(row=1, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        tree=ttk.Treeview(master=frame)
        col = ("fullname", "teamname", "dateofbirth", "height", "weight", "position", 
        "preferredfoot","debutyear","nationality","contractdate","contractenddate","backnumber")
        tree["columns"]= col
        tree.pack(side='bottom', fill='both')

        tree.column("#0", width=50, stretch=tk.NO)
        for i in col :
            tree.column(i, width=50)

        tree.heading("#0",text="no",anchor='center')
        for i in col :
            tree.heading(i, text=i, anchor='center')

        for no, row in enumerate(data) :
            tree.insert('', 'end', text=str('#'), values=[row[i] for i in col])
            print([row[i] for i in col])
        
        return window.mainloop()

    def rank_widget(self) :
        window = tk.Tk()
        window.title("EPL RANK")
        window.geometry("1200x500+100+100")
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        window.grid_columnconfigure(2, weight=1)
        window.grid_rowconfigure(0, weight=1)
        style = ttk.Style(window)
        style.configure('Treeview', rowheight=30)
        
        window['padx'] = 5
        window['pady'] = 5

        # - - - - - - - - - - - - - - - - - - - - -
        # The team rank frame
        team_frame = ttk.LabelFrame(window, text="team rank", relief=tk.RIDGE)
        team_frame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        
        team_tree=ttk.Treeview(team_frame)
        col1 = ("name","win","draw",'lose','score')
        team_tree["columns"]= col1
        team_tree.pack(side='top', fill='both')

        team_tree.column("#0", width=50, stretch=tk.NO)
        for i in col1 :
            if i == 'name' :
                team_tree.column(i, width=200)
            team_tree.column(i, width=50)

        team_tree.heading("#0",text="rank",anchor='center')
        for i in col1 :
            team_tree.heading(i, text=i, anchor='center')

        for rank, row in enumerate(db.team_rank()) :
            team_tree.insert('', 'end', text=str(rank+1), values=[row[i] for i in col1])
            
        # - - - - - - - - - - - - - - - - - - - - -
        # The goal rank frame
        goal_frame = ttk.LabelFrame(window, text="goal rank", relief=tk.RIDGE)
        goal_frame.grid(row=0, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        goal_tree=ttk.Treeview(goal_frame)
        col2 = ("fullname",'teamname',"totalgoal")
        goal_tree["columns"]=col2
        goal_tree.pack(side='top', fill='both')

        goal_tree.column("#0", width=50, stretch=tk.NO)
        for i in col2 :
            goal_tree.column(i, width=100)

        goal_tree.heading("#0",text="rank",anchor='center')
        for i in col2 :
            goal_tree.heading(i, text=i, anchor='center')

        for rank, row in enumerate(db.goal_rank()) :
            goal_tree.insert('', 'end', text=str(rank+1), values=[row[i] for i in col2])

        # - - - - - - - - - - - - - - - - - - - - -
        # The assist rank frame
        assist_frame = ttk.LabelFrame(window, text="assist rank", relief=tk.RIDGE)
        assist_frame.grid(row=0, column=2, sticky=tk.E + tk.W + tk.N + tk.S)

        assist_tree=ttk.Treeview(assist_frame)
        col3 = ("fullname",'teamname', "totalassist")
        assist_tree["columns"]=col3
        assist_tree.pack(side='top', fill='both')

        assist_tree.column("#0", width=50, stretch=tk.NO)
        for i in col3 :
            assist_tree.column(i, width=100)

        assist_tree.heading("#0",text="rank",anchor='center')
        for i in col3 :
            assist_tree.heading(i, text=i, anchor='center')

        for rank, row in enumerate(db.assist_rank()) :
            assist_tree.insert('', 'end', text=str(rank+1), values=[row[i] for i in col3])

        return window.mainloop()
    
    def game_list_widget(self) :
        window = tk.Tk()
        window.title("GAME LIST")
        window.geometry("1200x500+100+100")
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=10)

        style = ttk.Style(window)
        style.configure('Treeview', rowheight=30)

        label=tk.Label(window, text='GAMES', width=20, height=10)
        label.grid(row=0, column=0)

        data = db.game_list()
        
        window['padx'] = 5
        window['pady'] = 5

        # - - - - - - - - - - - - - - - - - - - - -
        # The game list frame
        game_frame = ttk.LabelFrame(window, text="Games", relief=tk.RIDGE)
        game_frame.grid(row=1, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        game_tree=ttk.Treeview(game_frame)
        col1 = ("gameid", "gamedate", "round","hometeam","awayteam",'homescore','awayscore','stadium')
        game_tree["columns"]= col1
        game_tree["displaycolumns"]=col1[1:]
        game_tree.pack(side='top', fill='both')

        game_tree.column("#0", width=50, stretch=tk.NO)
        for i in col1 :
            game_tree.column(i, width=50)

        game_tree.heading("#0",text="no",anchor='center')
        for i in col1 :
            game_tree.heading(i, text=i, anchor='center')

        for rank, row in enumerate(data) :
            game_tree.insert('', 'end', text=str(rank+1), values=[row[i] for i in col1])

        def game_select(event):
            gameid = game_tree.item(event.widget.selection())['values'][0]
            home = game_tree.item(event.widget.selection())['values'][3]
            away = game_tree.item(event.widget.selection())['values'][4]
            print(gameid, home, away)
            return self.game_detail_widget(gameid, home, away)
        
        game_tree.bind('<<TreeviewSelect>>', game_select)

        return window.mainloop()
    
    def game_detail_widget(self, gameid, home, away) :
        window = tk.Tk()
        window.title("GAME DETAIL")
        window.geometry("1600x500+100+100")
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=9)
        window['padx'] = 5
        window['pady'] = 5

        home_data, away_data = db.game_detail(int(gameid))

        home_label=tk.Label(window, text='Home : '+home, width=50, height=30)
        home_label.grid(row=0, column=0)
        away_label=tk.Label(window, text='Away : '+away, width=50, height=30)
        away_label.grid(row=0, column=1)
        
        for i, data in enumerate(db.game_detail(int(gameid))) :
            frame = ttk.LabelFrame(window, text="team info", relief=tk.RIDGE)
            frame.grid(row=1, column=i, sticky=tk.E + tk.W + tk.N + tk.S)

            tree=ttk.Treeview(frame)
            col = ("backnumber", "fullname","intime","outtime",'goal','assist','Yellowcard','Redcard','PerformanceRate')
            tree["columns"]= col
            tree["displaycolumns"]=col
            tree.pack(side='top', fill='both')

            tree.column("#0", width=50, stretch=tk.NO)
            for i in col :
                tree.column(i, width=50)

            tree.heading("#0",text="#",anchor='center')
            for i in col:
                tree.heading(i, text=i, anchor='center')

            for no, row in enumerate(data) :
                tree.insert('', 'end', text=str(no+1), values=[row[i] for i in col])

        style = ttk.Style(window)
        style.configure('Treeview', rowheight=30)

    #________________________________________
    def team_list_window(self, teamname) :
        window = tk.Tk()
        window.title("TEAM DETAIL")
        window.geometry("1200x500+100+100")
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=10)
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)

        style = ttk.Style(window)
        style.configure('Treeview', rowheight=30)

        team, lastgame, teamplayer = db.team_detail(teamname)

        label=tk.Label(window, text=teamname, width=20, height=10)
        label.grid(row=0, column=0, columnspan=2)
        
        window['padx'] = 5
        window['pady'] = 5

        # - - - - - - - - - - - - - - - - - - - - -
        # The lastgame frame
        game_frame = ttk.LabelFrame(window, text="last game", relief=tk.RIDGE)
        game_frame.grid(row=1, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        
        game_tree=ttk.Treeview(game_frame)
        col = ("round", "gamedate", "hometeam", "awayteam", "homescore", "awayscore")
        game_tree["columns"]= col
        game_tree.pack(side='top', fill='both')

        game_tree.column("#0", width=50, stretch=tk.NO)
        for i in col :
            game_tree.column(i, width=50)

        game_tree.heading("#0",text="#",anchor='center')
        for i in col :
            game_tree.heading(i, text=i, anchor='center')

        for no, row in enumerate(lastgame) :
            game_tree.insert('', 'end', text=str(no+1), values=[row[i] for i in col])

        # - - - - - - - - - - - - - - - - - - - - -
        # The teamplayer frame
        p_frame = ttk.LabelFrame(window, text="team player", relief=tk.RIDGE)
        p_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        p_tree=ttk.Treeview(p_frame)
        col2 = ("backnumber", "fullname", "position")
        p_tree["columns"]= col2
        p_tree.pack(side='top', fill='both')

        p_tree.column("#0", width=50, stretch=tk.NO)
        for i in col2 :
            p_tree.column(i, width=50)

        p_tree.heading("#0",text="#",anchor='center')
        for i in col2 :
            p_tree.heading(i, text=i, anchor='center')

        for no, row in enumerate(teamplayer) :
            p_tree.insert('', 'end', text=str(no+1), values=[row[i] for i in col2])


class AdminMode() :
    '''
    admin window for epl
    start with clicking admin mode btn
    '''
    def __init__(self, db):
        self.window = tk.Tk()
        self.window.title("Update match")
        self.window.geometry("500x400+100+100")
        self.create_adminwidgets()

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.db = db

    def create_adminwidgets(self):
        # Create some room around all the internal frames
        self.window['padx'] = 5
        self.window['pady'] = 5

        # - - - - - - - - - - - - - - - - - - - - -
        # The rank frame
        self.game_frame = ttk.LabelFrame(self.window, text="Game", relief=tk.RIDGE)
        self.game_frame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        game_btn = ttk.Button(self.game_frame, text="game insert", command=self.game_insert)
        game_btn.pack(side='top', fill='both')

        # - - - - - - - - - - - - - - - - - - - - -
        # The game frame
        self.squad_frame = ttk.LabelFrame(self.window, text="Squad", relief=tk.RIDGE)
        self.squad_frame.grid(row=0, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=6)

        squad_btn = ttk.Button(self.squad_frame, text="squad insert", command=self.squad_insert)
        squad_btn.pack(side='top', fill='both')

        # ----------
        # The goal frame
        self.goal_frame = ttk.LabelFrame(self.window, text="Goal", relief=tk.RIDGE)
        self.goal_frame.grid(row=1, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        goal_btn = ttk.Button(self.goal_frame, text="goal insert", command=self.goal_insert)
        goal_btn.pack(side='top', fill='both')

    def basic_design(self, query, col) :
        '''
        basic design for insert data
        you can use this method for insert or update your databases
        put a query and table columns for tuple
        '''
        window = tk.Tk()
        window.title("insert page")
        window.geometry("400x800+100+100")
        window['padx'] = 5
        window['pady'] = 5
        data = []
        Pair = namedtuple('Pair', ['column', 'object'])
        num = len(col)
        for i in range(num+1) :
            window.grid_rowconfigure(i, weight=1)
        for no, content in enumerate(col) :
            label = ttk.Label(window, text=content)
            label.grid(row=no, column=0, sticky=tk.E + tk.W )
            insert = ttk.Entry(window)
            insert.grid(row=no, column=1, sticky=tk.E + tk.W )
            a = Pair(content, insert)
            data.append(a) # 객체를 각자의 column 이름에 맞는 named tuple 로 저장

        def make_insert() :
            '''make insert data valid forms'''
            res =[]
            num = len(data)
            for i in range(num):
                if 'date' in data[i].column or 'Date' in data[i].column : # date라는 단어를 포함하는 column 이면 date타입으로 
                    date = datetime.datetime.strptime(data[i].object.get(), "%Y-%m-%d").date()
                    res.append(date)
                else :
                    try:
                        a = int(data[i].object.get()) # 숫자로 바꿀수 있으면 정수로
                        res.append(a)
                    except ValueError:
                        res.append(data[i].object.get())
            return tuple(res) # 모든 insertdata 튜플형태로
        
        insert_btn = ttk.Button(window, text='insert', command= lambda : self.insert_data(query, make_insert()))
        insert_btn.grid(row=num, column=0, columnspan=2, sticky=tk.E + tk.W + tk.N + tk.S)
    
        window.mainloop()

    def insert_data(self, query, res) :
        ''' error message for wrong datatypes''' 
        try : 
            self.db.texcute(query, res)
            self.db.commit()
        except :
            ewindow = tk.Tk()
            ewindow.title("error page")
            ewindow.geometry("400x400+100+100")
            ewindow['padx'] = 5
            ewindow['pady'] = 5
            label = ttk.Label(ewindow, text='올바른 형식의 데이터를 입력해주세요!')
            label.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
            ewindow.mainloop()
    
    def game_insert(self):
        col = ('GameDate', 'Round', 'HomeTeam', 'AwayTeam', 'HomeScore', 'AwayScore', 'GameStadium', 'HomeTeamFormation', 'AwayTeamFormation')
        query = '''INSERT INTO GAME 
        (GameDate, Round, HomeTeam, AwayTeam, HomeScore, AwayScore, GameStadium, HomeTeamFormation, AwayTeamFormation)
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        return self.basic_design(query, col)

    def squad_insert(self):
        col = ('GameID', 'PlayerID', 'TeamName', 'InTime', 'OutTime', 'Goal', 'Assist', 'YellowCard', 'RedCard', 'PerformanceRate')
        query = '''INSERT INTO TEAM_SQUAD
        (GameID, PlayerID, TeamName, InTime, OutTime, Goal, Assist, YellowCard, RedCard, PerformanceRate)
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        return self.basic_design(query, col)

    def goal_insert(self):
        col = ('GameID', 'PlayerID', 'AssistPlayerID', 'GoalTime')
        query = '''INSERT INTO GOAL
        (GameID, PlayerID, AssistPlayerID, GoalTime)
        VALUES
        (%s,%s,%s,%s)'''
        return self.basic_design(query, col)

# Create the entire GUI program
db = Database()
root = Counter_program(db)

# Start the GUI event loop
root.window.mainloop()