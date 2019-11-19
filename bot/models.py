import os 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, ForeignKey,create_engine
from sqlalchemy.orm import sessionmaker, Session,relationship
import requests
import datetime
from dateutil import tz
from collections import namedtuple

def CreateSession():
        engine = create_engine(f"sqlite:////home/turner_prize/leagueolas/league-site/league-site/data/league.db")#,echo=True)
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        return Session()

Base = declarative_base()

class Gameweeks(Base):
    __tablename__ = 'gameweeks'
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    deadline = Column(String(50))
    is_current = Column(String(50))
    is_next = Column(String(50))
    gameweek_start = Column(String(50))
    gameweek_end = Column(String(50))

class Players(Base):
    __tablename__ = 'players'
    jfpl = Column(Integer,primary_key=True)
    event_points = Column(Integer)
    first_name = Column(String(50))
    second_name = Column(String(50))
    web_name = Column(String(50))
    team = Column(Integer)
    team_code = Column(Integer)
    goals_scored = Column(Integer)
    assists = Column(Integer)
    goals_conceded = Column(Integer)
    pen_saved = Column(Integer)
    pen_missed = Column(Integer)
    yellow_cards = Column(Integer)
    red_cards = Column(Integer)
    saves = Column(Integer)
    element_type = Column(Integer)

class PlFixtures(Base):
    __tablename__ = 'plFixtures'
    id = Column(Integer,primary_key=True)
    kickoff_time = Column(String(50))
    gameweek = Column(Integer)
    away_team = Column(Integer)
    home_team = Column(Integer)
    started = Column(String(50))
    finished = Column(String(50))

class Fixtures(Base):
    __tablename__ = 'fixtures'
    id = Column(Integer,primary_key=True)
    gameweek = Column(Integer)
    managerId = Column(Integer)
    opponentId = Column(Integer)
    points = Column(Integer)
    score = Column(Integer)

class PlTeams(Base):
    __tablename__ = 'plTeams'
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    shortname = Column(Integer)

class Managers(Base):
    __tablename__ = 'managers'
    id = Column(Integer,primary_key=True)
    telegramId = Column(Integer)
    fplId = Column(Integer)
    name = Column(String(50))
    teamName= Column(String(50))
    draftPick = Column(Integer)
    TC = Column(Integer)
    BB = Column(Integer)
    FH = Column(Integer)
    WC1 = Column(Integer)
    WC2  = Column(Integer)
    
class Teams(Base):
    __tablename__ = 'teams'
    id = Column(Integer,primary_key=True)
    gameweek = Column(Integer)
    managerId = Column(Integer)
    playerId =  Column(Integer)
    points = Column(Integer)
    is_captain = Column(Integer)
    is_bench = Column(Integer)
    reefed = Column(Integer)

class DraftedPlayers(Base):
    __tablename__ = 'draftedPlayers'
    id = Column(Integer,primary_key=True)
    managerId = Column(Integer)
    playerId =  Column(Integer)

class Table(Base):
    __tablename__ = 'table'
    position = Column(Integer)
    managerId =  Column(Integer,primary_key=True)
    score =  Column(Integer)
    points =  Column(Integer)






        


