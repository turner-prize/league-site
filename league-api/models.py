from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import requests
import os

db = SQLAlchemy()
ma = Marshmallow()

class Gameweeks(db.Model):
    __tablename__ = 'gameweeks'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    deadline = db.Column(db.String(50))
    is_current = db.Column(db.String(50))
    is_next = db.Column(db.String(50))
    gameweek_start = db.Column(db.String(50))
    gameweek_end = db.Column(db.String(50))

class Players(db.Model):
    __tablename__ = 'players'
    jfpl = db.Column(db.Integer,primary_key=True)
    event_points = db.Column(db.Integer)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    team = db.Column(db.Integer, db.ForeignKey('plTeams.id'))
    team_code = db.Column(db.Integer)
    goals_scored = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    goals_conceded = db.Column(db.Integer)
    pen_saved = db.Column(db.Integer)
    pen_missed = db.Column(db.Integer)
    yellow_cards = db.Column(db.Integer)
    red_cards = db.Column(db.Integer)
    saves = db.Column(db.Integer)
    element_type = db.Column(db.Integer)
    drafted = db.Column(db.Integer)
    team_details = db.relationship('PlTeams', backref='players')
    
class Managers(db.Model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer,primary_key=True)
    telegramid = db.Column(db.Integer)
    fplid = db.Column(db.Integer)
    name = db.Column(db.String(50))
    teamName = db.Column(db.String(50))
    draftPick = db.Column(db.Integer)
    TC = db.Column(db.Integer)
    BB = db.Column(db.Integer)
    FH = db.Column(db.Integer)
    WC1 = db.Column(db.Integer)
    WC2 = db.Column(db.Integer)
    
class PlTeams(db.Model):
    __tablename__ = 'plTeams'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    shortname = db.Column(db.Integer)

class DraftedPlayers(db.Model):
    __tablename__ = 'draftedPlayers'
    id = db.Column(db.Integer,primary_key=True)
    managerId = db.Column(db.Integer,db.ForeignKey('managers.id'))
    playerId = db.Column(db.Integer,db.ForeignKey('players.jfpl'))
    manager_details = db.relationship('Managers', backref='draftedPlayers')
    player_details = db.relationship('Players', backref='draftedPlayers')
    
class Fixtures(db.Model):
    __tablename__ = 'fixtures'
    id = db.Column(db.Integer,primary_key=True)
    gameweek = db.Column(db.Integer,db.ForeignKey('gameweeks.id'))
    managerId = db.Column(db.Integer,db.ForeignKey('managers.id'))
    managerId = db.Column(db.Integer,db.ForeignKey('managers.id'))

class DraftBoard(db.Model):
    __tablename__ = 'draftBoard'
    id = db.Column(db.Integer,primary_key=True)
    managerId = db.Column(db.Integer,db.ForeignKey('managers.id'))
    GK = db.Column(db.String(50))
    MF1 = db.Column(db.String(50))
    MF2 = db.Column(db.String(50))
    DF1 = db.Column(db.String(50))
    DF2 = db.Column(db.String(50))
    FWD = db.Column(db.String(50))
    manager_details = db.relationship('Managers', backref='draftBoard')

#Schemas>

class gameweekSchema(ma.Schema):
    class Meta:
        fields = ('id','name')

class plTeamsSchema(ma.ModelSchema):
    class Meta:
        models = PlTeams
        fields = ('id','name','shortname')

class playerSchema(ma.ModelSchema):
    class Meta:
        model = Players
        fields = ('jfpl','first_name','second_name','element_type','shortname','name','drafted')
        
class managerSchema(ma.ModelSchema):
    class Meta:
        models = Managers
        fields = ('id','telegramid','fplid','name','teamName','draftPick')

class draftedPlayerSchema(ma.ModelSchema):
    class Meta:
        models = Managers
        fields = ('id','managerId','playerId','teamName','first_name','second_name','element_type','shortname','name')
        
class draftedBoardSchema(ma.ModelSchema):
    class Meta:
        models = Managers
        fields = ('id','teamName','draftPick','GK','DF1','DF2','MF1','MF2','FWD')