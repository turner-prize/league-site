from models import CreateSession, Gameweeks, Fixtures, Teams, Managers,Players,PlFixtures
from sqlalchemy import or_



def Played(session,gw,managedId):
    return len(session.query(Teams,Players,PlFixtures) \
                        .filter(Teams.playerId==Players.jfpl) \
                        .filter(or_(PlFixtures.away_team==Players.team,PlFixtures.home_team==Players.team)) \
                        .filter_by(managerId = managedId) \
                        .filter_by(gameweek = gw) \
                        .filter(PlFixtures.finished == 1) \
                        .filter_by(is_bench=0) \
                        .all())

def Playing(session,gw,managedId):
    return len(session.query(Teams,Players,PlFixtures) \
                        .filter(Teams.playerId==Players.jfpl) \
                        .filter(or_(PlFixtures.away_team==Players.team,PlFixtures.home_team==Players.team)) \
                        .filter_by(managerId = managedId) \
                        .filter_by(gameweek = gw) \
                        .filter(PlFixtures.started == 1) \
                        .filter(PlFixtures.finished == 0) \
                        .filter_by(is_bench=0) \
                        .all())

def StillToPlay(session,gw,managedId):
    return len(session.query(Teams,Players,PlFixtures) \
                        .filter(Teams.playerId==Players.jfpl) \
                        .filter(or_(PlFixtures.away_team==Players.team,PlFixtures.home_team==Players.team)) \
                        .filter_by(managerId = managedId) \
                        .filter_by(gameweek = gw) \
                        .filter(PlFixtures.started == 0) \
                        .filter_by(is_bench=0) \
                        .all())

def getScoreString(session,id,gw):
    #need to add BB and TC check here
    manager = session.query(Managers).filter_by(id=id).first()
    scores = session.query(Teams).filter_by(managerId=id).filter_by(gameweek=gw).filter_by(is_bench=0).all()
    for i in scores:
        if i.is_captain==1:
            if TripleCaptain(session,id,gw):
                i.points = (i.points * 3)
            else:
                i.points = (i.points * 2)
    scoreList = [x.points for x in scores]
    points = sum(scoreList)
    played = Played(session,gw,id)
    playing = Playing(session,gw,id)
    stillToPlay = StillToPlay(session,gw,id)
    return f'{manager.teamName} - {points} - [{played}-{playing}-{stillToPlay}]'
    
def TripleCaptain(session,managerId,gw):
    TC = session.query(Managers).filter_by(id=managerId).filter_by(TC=gw).first()
    return TC
    
def getAllScores():
    session=CreateSession()
    gw = session.query(Gameweeks.id).filter_by(is_current=1).first()
    gw = gw[0]
    fixtures = session.query(Fixtures).filter_by(gameweek=gw).all()
    fx = []
    ScoreString = ''
    for f in fixtures:
        manager1 = session.query(Managers).filter_by(id=f.managerId).first()
        if manager1.id in fx:
            continue
        else:
            ss1 = getScoreString(session,f.managerId,gw)
            ss2 = getScoreString(session,f.opponentId,gw)
            
            fx.append(f.managerId)
            fx.append(f.opponentId)
            ScoreString = ScoreString + '\n' + f'{ss1} \nvs\n{ss2}\n---'
    session.close()
    return ScoreString
 
def getOneScore(TelegramId):
    session=CreateSession()
    gw = session.query(Gameweeks.id).filter_by(is_current=1).first()
    gw = gw[0]
    manager = session.query(Managers).filter_by(telegramId=TelegramId).first()
    fixtures = session.query(Fixtures).filter_by(gameweek=gw).filter_by(managerId=manager.id).first()  
    ScoreString = ''
    ss1 = getScoreString(session,fixtures.managerId,gw)
    ss2 = getScoreString(session,fixtures.opponentId,gw)
    ScoreString = f'{ss1} \nvs\n{ss2}'
    session.close()
    return ScoreString