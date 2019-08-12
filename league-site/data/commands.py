from models import CreateSession, Gameweeks, Fixtures, Teams, Managers,Players,PlFixtures,DraftedPlayers, PlTeams
from sqlalchemy import or_,desc


def GetPos(position):
    if position == 1:
        p = 'GKP'
    elif position == 2:
        p = 'DEF'
    elif position == 3:
        p = 'MID'
    elif position == 4:
        p = 'FWD'
    return p

def ElementType(position):
    if position == 'GKP':
        p = 1
    elif position == 'DEF':
        p = 2
    elif position == 'MID':
        p = 3
    elif position == 'FWD':
        p = 4
    return p

def DraftList(pos=None):
    session = CreateSession()
    if pos:
        p = ElementType(pos)
        manager = session.query(Managers,DraftedPlayers,Players, PlTeams) \
                            .filter(Managers.id==DraftedPlayers.managerId) \
                            .filter(Players.jfpl==DraftedPlayers.playerId) \
                            .filter(Players.team==PlTeams.id) \
                            .filter(Players.element_type==p) \
                            .order_by(desc(Managers.id)) \
                            .order_by(Players.element_type) \
                            .all()
    else:
        manager = session.query(Managers,DraftedPlayers,Players, PlTeams) \
                            .filter(Managers.id==DraftedPlayers.managerId) \
                            .filter(Players.jfpl==DraftedPlayers.playerId) \
                            .filter(Players.team==PlTeams.id) \
                            .order_by(desc(Managers.id)) \
                            .order_by(Players.element_type) \
                            .all()
    dlist = {}
    for i in manager:
        if not i[0].teamName in dlist:
            dlist[i[0].teamName]=[]
        pos = GetPos(i[2].element_type)
        draftString = f'{pos} - {i[2].web_name} - {i[3].shortname}'
        dlist[i[0].teamName].append(draftString)
        
    dString=''
    for k,v in dlist.items():
        dString=dString + f"\n{k}:"
        for dl in v:
            dString=dString + f"\n\t{dl}"
        dString=dString + f'\n'
    return dString


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