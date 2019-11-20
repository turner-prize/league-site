from config import db
from models import DraftBoard,DraftedPlayers,Fixtures,Gameweeks,Managers,PLFixtures,PLTeams,Players,Table,TableHistory,Teams
from models import TH,FixturesReadable
from schemas import DraftBoardSchema,DraftedPlayersSchema,FixturesSchema,GameweeksSchema, ManagersSchema,PLFixturesSchema,PLTeamsSchema,PlayersSchema,TableSchema,TableHistorySchema,TeamsSchema
from schemas import FixturesReadableSchema,THSchema
from sqlalchemy.orm import aliased
from datetime import date
import json

def getDraftBoard():
    d = DraftBoard.query.all()
    this_schema = DraftBoardSchema(many=True)
    return this_schema.dump(d).data

def getDraftedPlayers():
    d = DraftedPlayers.query.all()
    this_schema = DraftedPlayersSchema(many=True)
    return this_schema.dump(d).data
    
def getFixtures():
    d = Fixtures.query.all()
    this_schema = FixturesSchema(many=True)
    return this_schema.dump(d).data
    
def getGameweeks():
    d = Gameweeks.query.all()
    this_schema = GameweeksSchema(many=True)
    return this_schema.dump(d).data

def getManagers():
    d = Managers.query.all()
    this_schema = ManagersSchema(many=True)
    return this_schema.dump(d).data

def getPLFixtures():
    d = PLFixtures.query.all()
    this_schema = PLFixturesSchema(many=True)
    return this_schema.dump(d).data

def getPLTeams():
    d = PLTeams.query.all()
    this_schema = PLTeamsSchema(many=True)
    return this_schema.dump(d).data

def getPlayers():
    d = Players.query.all()
    this_schema = PlayersSchema(many=True)
    return this_schema.dump(d).data

def getTable():
    d = Table.query.all()
    this_schema = TableSchema(many=True)
    return this_schema.dump(d).data

def getTeams():
    d = Teams.query.all()
    this_schema = TeamsSchema(many=True)
    return this_schema.dump(d).data
   
def getTableHistory():
    tn = [i.teamname for i in db.session.query(Managers.teamname).all()]
    xgw = 0
    allDatasets = []
    
    for teamname in tn:
    
        x = db.session.query(TableHistory).join(Managers, Managers.id==TableHistory.manager) \
                                          .add_columns(   TableHistory.id,
                                                    TableHistory.position,
                                                    TableHistory.gameweek,
                                                    Managers.teamname) \
                                          .filter(Managers.teamname == teamname) \
                                    .all()
        thisDataset = []
        for i in x:
            thisDatapoint = {}
            gw = i.gameweek
            pos = i.position
            if gw > xgw:
                xgw = gw
            thisDatapoint['x'] = gw
            thisDatapoint['y'] = pos
            thisDataset.append(thisDatapoint)
        fin = {
               'label':teamname,
               'data':thisDataset,
               'borderColor': db.session.query(Managers.colour).filter(Managers.teamname == teamname).first(),
               'backgroundColor': db.session.query(Managers.colour).filter(Managers.teamname == teamname).first(),
               'fill':False
               }
        allDatasets.append(fin)
    labels = [i for i in range(1,xgw +1)]
    
    finalproduct = {'data': {
                              'labels':labels,
                              'datasets': allDatasets
                              }
                    }
    
    return finalproduct
   

#Ignore below, just a test for formatting queries to be consumable via API
def getfixturesReadable():
    M2 = aliased(Managers)
    x = Fixtures.query.join(Managers, Managers.id==Fixtures.managerid) \
                      .join(M2, M2.id==Fixtures.opponentid) \
                      .add_columns( Fixtures.id,
                                    Fixtures.opponentid,
                                    Fixtures.gameweek,
                                    Managers.name,
                                    Managers.teamname,
                                    Fixtures.score,
                                    Fixtures.points,
                                    M2.name.label('oname'),
                                    M2.teamname.label('oteamname')
                                  ) \
                      .all()
    fixtures_schema = FixturesReadableSchema(many=True)    
    return fixtures_schema.dump(x).data
    
  
#insert into tableHistory (gameweek,manager,position)
#select 12 as gameweek,managerid, rank() over( order by sum(points) desc,sum(score) desc) rnk from fixtures f
#left join managers m on f.managerId = m.id
#where gameweek  <=12
#group by teamname
#order by sum(points) desc,sum(score) desc'''