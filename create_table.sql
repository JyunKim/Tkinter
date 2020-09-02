CREATE TABLE PLAYER(
		PlayerID		Int				NOT NULL AUTO_INCREMENT,
        LastName 		Varchar(45)		NULL,
        FirstName 		Varchar(45)		NULL,
        MidName			Varchar(45) 	NULL,
        CallName		Varchar(45) 	NULL,
        TeamName		Varchar(45)		NULL,
        DateOfBirth		Date			NULL,
        Height			Float			NULL,
        Weight			Float			NULL,
        Position	  	Varchar(5)		NULL,
        PreferredFoot 	Varchar(45) 	NULL,
        DebutYear		Int				NULL,
        Nationality		Varchar(45) 	NULL,
        ContractDate 	Date			NULL,
        ContractEndDate Date			NULL,
        BackNumber		Int				NULL,
        CONSTRAINT		PLAYER_PK		PRIMARY KEY(PlayerID),
        CONSTRAINT		PLAYER_AK1		UNIQUE(TeamName,BackNumber),
        CONSTRAINT		PositionValues	CHECK
						(Position IN ('FW','MF','DF','GK')),
		CONSTRAINT		PreferredFootValues	CHECK
						(PreferredFoot IN ('left','right','both')),
		CONSTRAINT		ContractDateCheck	CHECK
						(ContractDate < ContractEndDate)
        );
        
CREATE TABLE TEAM(
		TeamName 		Varchar(45) 	NOT NULL,
        Area  			Varchar(45) 	NULL,
		StadiumName 	Varchar(45) 	NULL,
		EstablishedYear Date 			NULL,
        ManagerID		Int				NULL,
        CONSTRAINT		TEAM_PK			PRIMARY KEY(TeamName),
        CONSTRAINT		TEAM_AK1		UNIQUE(StadiumName),
        CONSTRAINT		TEAM_AK2		UNIQUE(ManagerID)
        );

ALTER TABLE PLAYER
	ADD CONSTRAINT 		PLAYER_TEAM_FK	FOREIGN KEY(TeamName)
						REFERENCES		TEAM(TeamName);
                        
CREATE TABLE INJURY(
		InjuryID		Int				NOT NULL AUTO_INCREMENT,
        PlayerID		Int				NULL,
        InjuryType		Varchar(45)		NULL,
        InjuryReason	Varchar(45)		NULL,
        InjuryDate		Date			NULL,
        ExpectedEndDate	Date			NULL,
        CONSTRAINT		INJURY_PK		PRIMARY KEY(InjuryID),
        CONSTRAINT		InjuryDateCheck	CHECK
						(InjuryDate < ExpectedEndDate)
        );
        
CREATE TABLE MANAGER(
		ManagerID		Int				NOT NULL AUTO_INCREMENT,
        LastName 		Varchar(45)		NULL,
        FirstName 		Varchar(45)		NULL,
        MidName			Varchar(45) 	NULL,
        CallName		Varchar(45) 	NULL,
        AppointedDate	Date			NULL,
        ContractEndDate	Date			NULL,
        CONSTRAINT		MANAGER_PK		PRIMARY KEY(ManagerID),
        CONSTRAINT		ManagerDateCheck	CHECK
						(AppointedDate < ContractEndDate)
        );

ALTER TABLE INJURY
	ADD CONSTRAINT 		INJURY_PLAYER_FK	FOREIGN KEY(PlayerID)
						REFERENCES			PLAYER(PlayerID);
                        
ALTER TABLE TEAM
	ADD CONSTRAINT 		TEAM_MANAGER_FK		FOREIGN KEY(ManagerID)
						REFERENCES			MANAGER(ManagerID);
        
CREATE TABLE GAME(
		GameID				Int				NOT NULL AUTO_INCREMENT,
        GameDate			Date			NULL,
        Round				Int				NULL,
        HomeTeam			Varchar(45)		NULL,
        AwayTeam			Varchar(45)		NULL,
        HomeScore			Int				NULL,
        AwayScore			Int				NULL,
        GameStadium			Varchar(45)		NULL,
        HomeTeamFormation	Varchar(45)		NULL,
        AwayTeamFormation	Varchar(45)		NULL,
        CONSTRAINT			GAME_PK			PRIMARY KEY(GameID),
        CONSTRAINT			GAME_AK1		UNIQUE(HomeTeam,AwayTeam),
        CONSTRAINT			GAME_AK2		UNIQUE(GameDate,HomeTeam),
        CONSTRAINT			GAME_AK3		UNIQUE(GameDate,AwayTeam),
        CONSTRAINT			GAME_AK4		UNIQUE(Round,HomeTeam),
        CONSTRAINT			GAME_AK5		UNIQUE(Round,AwayTeam),
        CONSTRAINT			RoundRange		CHECK
							(Round >= 1 AND Round <=38),
		CONSTRAINT			TeamCondition	CHECK
							(HomeTeam <> AwayTeam)
        );
        
ALTER TABLE GAME
	ADD CONSTRAINT 		GAME_TEAM_FK		FOREIGN KEY(HomeTeam)
						REFERENCES			TEAM(TeamName),
	ADD CONSTRAINT 		GAME_TEAM_FK2		FOREIGN KEY(AwayTeam)
						REFERENCES			TEAM(TeamName);
                        
CREATE TABLE TEAM_SQUAD(
        GameID				Int				NOT NULL,
        PlayerID			Int				NOT NULL,
        TeamName			Varchar(45)		NOT NULL,
        InTime				Int				NULL,
        OutTime				Int				NULL,
        Goal				Int				NULL,
        Assist				Int				NULL,
        YellowCard			Int				NULL,
        RedCard				Int				NULL,
        PerformanceRate		Decimal(3,1)	NULL,
        CONSTRAINT			TEAM_SQUAD_PK	PRIMARY KEY(PlayerID, GameID, TeamName),
        CONSTRAINT		YellowCardValues	CHECK
						(YellowCard	IN (0,1,2)),
		CONSTRAINT		RedCardValues		CHECK
						(RedCard IN (0,1)),
		CONSTRAINT		PerformanceRateRange	CHECK
						(PerformanceRate >= 0 AND PerformanceRate <= 10),
	    CONSTRAINT		TimeCheck			CHECK
						(InTime < OutTime)
        );
        
ALTER TABLE TEAM_SQUAD
	ADD CONSTRAINT 		TEAM_SQUAD_PLAYER_FK	FOREIGN KEY(PlayerID)
						REFERENCES				PLAYER(PlayerID),
	ADD CONSTRAINT 		TEAM_SQUAD_GAME_FK		FOREIGN KEY(GameID)
						REFERENCES				GAME(GameID),
	ADD CONSTRAINT 		TEAM_SQUAD_TEAM_FK		FOREIGN KEY(TeamName)
						REFERENCES				TEAM(TeamName);
                        
CREATE TABLE MANAGER_ON_GAME(
		GameID 				INT 	NOT NULL,
        HomeTeamManagerID 	INT 	NULL,
        AwayTeamManagerID 	INT 	NULL,
        CONSTRAINT			MANAGER_ON_GAME_PK		PRIMARY KEY(GameID),
        CONSTRAINT			ManagerCondition		CHECK
							(HomeTeamManagerID <> AwayTeamManagerID)
		);

ALTER TABLE MANAGER_ON_GAME
	ADD CONSTRAINT 		MANAGER_ON_GAME_MANAGER_FK	FOREIGN KEY(HomeTeamManagerID)
						REFERENCES					MANAGER(ManagerID),
	ADD CONSTRAINT 		MANAGER_ON_GAME_MANAGER_FK2	FOREIGN KEY(AwayTeamManagerID)
						REFERENCES					MANAGER(ManagerID),
	ADD CONSTRAINT 		MANAGER_ON_GAME_GAME_FK3	FOREIGN KEY(GameID)
						REFERENCES					GAME(GameID);  

CREATE TABLE GOAL(
		GoalID				Int				NOT NULL AUTO_INCREMENT,
        GameID	            Int				NULL,
        PlayerID			Int				NULL,
        AssistPlayerID		Int				NULL,
        GoalTime			Varchar(45)		NULL,
        CONSTRAINT			GOAL_PK			PRIMARY KEY(GoalID),
        CONSTRAINT			PlayerCheck		CHECK
							(PlayerID <> AssistPlayerID)
        );
        
ALTER TABLE GOAL
	ADD CONSTRAINT 		GOAL_PLAYER_FK		FOREIGN KEY(PlayerID)
						REFERENCES			PLAYER(PlayerID),
	ADD CONSTRAINT 		GOAL_GAME_FK		FOREIGN KEY(GameID)
						REFERENCES			GAME(GameID),
	ADD CONSTRAINT  	GOAL_PLAYER_FK2		FOREIGN KEY(AssistPlayerID)
						REFERENCES			PLAYER(PlayerID);

        
        

                        