from datetime import datetime
from config import db

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
    
class TableHistory(db.Model):
    __tablename__ = 'tableHistory'
    id = db.Column(db.Integer, primary_key=True)
    gameweek = db.Column(db.Integer)
    manager = db.Column(db.Integer)
    position = db.Column(db.Integer)

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