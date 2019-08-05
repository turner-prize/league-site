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


class gameweekSchema(ma.Schema):
    class Meta:
        fields = ('id','name')

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
    team_details = db.relationship('PlTeams', backref='players')
    
class PlTeams(db.Model):
    __tablename__ = 'plTeams'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    shortname = db.Column(db.Integer)

class plTeamsSchema(ma.ModelSchema):
    class Meta:
        models = PlTeams
        fields = ('id','name','shortname')

class playerSchema(ma.ModelSchema):
    class Meta:
        model = Players
        fields = ('first_name','second_name','element_type','shortname','name')