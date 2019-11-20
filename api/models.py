from datetime import datetime
from config import db

class DraftBoard(db.Model):
    __tablename__= 'draftBoard'
    id = db.Column(db.Integer, primary_key=True)
    managerId = db.Column(db.Integer)
    GK = db.Column(db.String)
    DF1 = db.Column(db.String)
    DF2 = db.Column(db.String)
    MF1 = db.Column(db.String)
    MF2 = db.Column(db.String)
    FWD = db.Column(db.String)

class DraftedPlayers(db.Model):
    __tablename__ = 'draftedPlayers'
    id = db.Column(db.Integer, primary_key=True)
    managerid = db.Column(db.Integer)
    playerid = db.Column(db.Integer)
    
class Fixtures(db.Model):
    __tablename__ = 'fixtures'
    id = db.Column(db.Integer, primary_key=True)
    gameweek = db.Column(db.Integer)
    managerid = db.Column(db.Integer)
    opponentid = db.Column(db.Integer)
    points = db.Column(db.Integer)
    score = db.Column(db.Integer)
    
class Gameweeks(db.Model):
    __tablename__ = 'gameweeks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    deadline = db.Column(db.String)
    is_current = db.Column(db.Integer)
    is_next = db.Column(db.Integer)
    
class Managers(db.Model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    telegramid = db.Column(db.Integer)
    fplid = db.Column(db.Integer)
    name = db.Column(db.String)
    teamname = db.Column(db.String)
    draftpick = db.Column(db.Integer)
    tc = db.Column(db.Integer)
    bb = db.Column(db.Integer)
    fh = db.Column(db.Integer)
    wc1 = db.Column(db.Integer)
    wc2 = db.Column(db.Integer)
    colour = db.Column(db.String)
    
class PLFixtures(db.Model):
    __tablename__ = 'plFixtures'
    id = db.Column(db.Integer, primary_key=True)
    kickoff_time = db.Column(db.String)
    gameweek = db.Column(db.Integer)
    away_team = db.Column(db.Integer)
    home_team = db.Column(db.Integer)
    started = db.Column(db.Integer)
    finished = db.Column(db.Integer)
    
class PLTeams(db.Model):
    __tablename__ = 'plTeams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    shortname = db.Column(db.String)

class Players(db.Model):
    __tablename__ = 'players'
    jfpl = db.Column(db.Integer, primary_key=True)
    event_points = db.Column(db.Integer)
    first_name = db.Column(db.String)
    second_name = db.Column(db.String)
    team = db.Column(db.Integer)
    team_code = db.Column(db.Integer)
    goals_scored = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    goals_conceded = db.Column(db.Integer)
    pen_save = db.Column(db.Integer)
    pen_missed = db.Column(db.Integer)
    yellow_cards = db.Column(db.Integer)
    red_cards = db.Column(db.Integer)
    saves = db.Column(db.Integer)
    element_type = db.Column(db.Integer)
    web_name = db.Column(db.String)

class Table(db.Model):
    __tablename__ = 'table'
    position = db.Column(db.Integer, primary_key=True)
    managerid = db.Column(db.Integer)
    score = db.Column(db.Integer)
    points = db.Column(db.Integer)

class TableHistory(db.Model):
    __tablename__ = 'tableHistory'
    id = db.Column(db.Integer, primary_key=True)
    gameweek = db.Column(db.Integer)
    manager = db.Column(db.Integer)
    position = db.Column(db.Integer)

class Teams(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    gameweek = db.Column(db.Integer)
    managerid = db.Column(db.Integer)
    playerid = db.Column(db.Integer)
    points = db.Column(db.Integer)
    is_captain = db.Column(db.Integer)
    is_bench = db.Column(db.Integer)
    reefed = db.Column(db.Integer)
    
#custom views below

class TH(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameweek = db.Column(db.Integer)
    position = db.Column(db.Integer)
    teamname = db.Column(db.String)

#Ignore below, just a test for formatting queries to be consumable via API
class FixturesReadable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameweek = db.Column(db.Integer)
    managerid = db.Column(db.Integer)
    opponentid = db.Column(db.Integer)
    points = db.Column(db.Integer)
    score = db.Column(db.Integer)
    name = db.Column(db.String)
    teamname = db.Column(db.String)
    oname = db.Column(db.String)
    oteamname = db.Column(db.String)