from config import db
from models import DraftedPlayers, Fixtures, Managers, FixturesReadable, TableHistory, TH
from schemas import DraftedPlayersSchema,FixturesSchema, ManagersSchema, FixturesReadableSchema, TableHistorySchema, THSchema
from sqlalchemy.orm import aliased
from datetime import date

def getDrafted():
    d = DraftedPlayers.query.all()
    draftedplayers_schema = DraftedPlayersSchema(many=True)
    return draftedplayers_schema.dump(d).data
    
def getFixtures():
    f = Fixtures.query.all()
    fixtures_schema = FixturesSchema(many=True)    
    return fixtures_schema.dump(f).data
    
def getTableHistory():
    th = TableHistory.query.join(Managers, Managers.id==TableHistory.manager) \
                                .add_columns(   TableHistory.id,
                                                TableHistory.position,
                                                TableHistory.gameweek,
                                                Managers.teamname) \
                                .all()
    th_schema = THSchema(many=True)    
    return th_schema.dump(th).data

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