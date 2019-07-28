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
        
def populateGameweeks():
    r = requests.get("https://fantasy.premierleague.com/api/bootstrap-static")
    bootstrapData = r.json()
    gameweekData = bootstrapData['events']
    for i in gameweekData:
        gw = Gameweeks( id=i['id'],
                        name=i['name'],
                        deadline=i['deadline_time'],
                        is_current=i['is_current'],
                        is_next=i['is_next'],
                        gameweek_start='test',
                        gameweek_end='test')
        db.session.add(gw)
        db.session.commit()
    db.session.close()