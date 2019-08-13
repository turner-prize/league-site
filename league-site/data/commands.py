from models import CreateSession, Gameweeks, Fixtures, Teams, Managers,Players,PlFixtures,DraftedPlayers, PlTeams
from sqlalchemy import or_,desc
from fuzzywuzzy import process


def WhoHas(playerName):
    session = CreateSession()
    
    draftedPlayer = session.query(DraftedPlayers,Players, Managers).filter(DraftedPlayers.playerId==Players.jfpl).filter(DraftedPlayers.managerId==Managers.id).all()
    for i in draftedPlayer:
        if i[1].web_name == playerName:
            gotString = f'{i[1].first_name} {i[1].second_name} was drafted by {i[2].teamName}'

    else:
        playerdict = {i.web_name:i.jfpl for i in session.query(Players).all()}
        playerlist = [i.web_name for i in session.query(Players).all()]

		
        extraction = process.extract(playerName, playerlist)

        playerId = playerdict[extraction[0][0]]

        draftedPlayer = session.query(DraftedPlayers,Players, Managers).filter(DraftedPlayers.playerId==Players.jfpl).filter_by(playerId=playerId).filter(DraftedPlayers.managerId==Managers.id).first()
        if draftedPlayer:
            gotString = f'{draftedPlayer[1].first_name} {draftedPlayer[1].second_name} was drafted by {draftedPlayer[2].teamName}'

        else:
        
            gw = session.query(Gameweeks.id).filter_by(is_current=1).first()
            gw = gw[0]
            
            scores = session.query(Teams,Players, Managers).filter(Teams.playerId==playerId).filter(Teams.playerId==Players.jfpl).filter(Teams.managerId==Managers.id).filter_by(playerId=playerId).filter_by(gameweek=gw).all()
            
            if scores:
                gotString = ''
                for i in scores:
                    gotString = gotString + f'\n{i[2].teamName} has {i[1].first_name} {i[1].second_name}'
            
            else:
                draftedPlayer = session.query(Players).filter(Players.jfpl==playerId).first()
                gotString = f'No one has {draftedPlayer.first_name} {draftedPlayer.second_name}'
            
    session.close()
    print(gotString)
    
       
WhoHas('Pieters')
input()
        
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
    session.close()
    return dString

def PlayersDetailed(TelegramId):
    session=CreateSession()
    gw = session.query(Gameweeks.id).filter_by(is_current=1).first()
    gw = gw[0]
    manager = session.query(Managers).filter_by(telegramId=TelegramId).first()
    fixtures = session.query(Fixtures).filter_by(gameweek=gw).filter_by(managerId=manager.id).first()  
    ScoreString = ''
    ss1 = getDetailedTeam(session,fixtures.managerId,gw)
    ss2 = getDetailedTeam(session,fixtures.opponentId,gw)
    ScoreString = f'{ss1} \nvs\n\n{ss2}'
    session.close()
    return ScoreString

def getDetailedTeam(session,id,gw):
    #need to add BB and TC check here
    manager = session.query(Managers).filter_by(id=id).first()
    scores = session.query(Teams,Players).filter(Teams.playerId==Players.jfpl).filter_by(managerId=id).filter_by(gameweek=gw).filter_by(is_bench=0).order_by(Players.element_type).all()
    bench = session.query(Teams,Players).filter(Teams.playerId==Players.jfpl).filter_by(managerId=id).filter_by(gameweek=gw).filter_by(is_bench=1).order_by(Players.element_type).all()
    for i in scores:
        if i[0].is_captain==1:
            if TripleCaptain(session,id,gw):
                i[0].points = (i[0].points * 3)
            else:
                i[0].points = (i[0].points * 2)

    scoreDict = {x[1].jfpl:{'web_name':x[1].web_name+ ' (c)' if x[0].is_captain ==1 else x[1].web_name,'points':x[0].points} for x in scores}
    benchDict = {x[1].jfpl:{'web_name':x[1].web_name,'points':x[0].points} for x in bench}
    for id in scoreDict:
        if PlayedDetailed(session,gw,manager.id,id):
            scoreDict[id]['status'] = 'Played'
            continue
        elif PlayingDetailed(session,gw,manager.id,id):
            scoreDict[id]['status'] = 'Playing'
        else:
            scoreDict[id]['status']= 'Yet to Play'
    for id in benchDict:
        if PlayedDetailed(session,gw,manager.id,id):
            benchDict[id]['status'] = 'Played'
            continue
        elif PlayingDetailed(session,gw,manager.id,id):
            benchDict[id]['status'] = 'Playing'
        else:
            benchDict[id]['status']= 'Yet to Play'
    MyString = manager.teamName + ':\n'
    for k, v in scoreDict.items():
        MyString = MyString + f"{v['web_name']} - {v['points']} - {v['status']}\n"
    MyString = MyString + '----------\n'
    for k, v in benchDict.items():
        MyString = MyString + f"{v['web_name']} - {v['points']} - {v['status']}\n"
    
    return MyString

def PlayedDetailed(session,gw,managedId,playerId):
    return len(session.query(Teams,Players,PlFixtures) \
                        .filter(Teams.playerId==Players.jfpl) \
                        .filter(or_(PlFixtures.away_team==Players.team,PlFixtures.home_team==Players.team)) \
                        .filter_by(managerId = managedId) \
                        .filter_by(gameweek = gw) \
                        .filter(Teams.playerId == playerId) \
                        .filter(PlFixtures.finished == 1) \
                        .all())

def PlayingDetailed(session,gw,managedId,playerId):
    return len(session.query(Teams,Players,PlFixtures) \
                        .filter(Teams.playerId==Players.jfpl) \
                        .filter(or_(PlFixtures.away_team==Players.team,PlFixtures.home_team==Players.team)) \
                        .filter_by(managerId = managedId) \
                        .filter_by(gameweek = gw) \
                        .filter(Teams.playerId == playerId) \
                        .filter(PlFixtures.started == 1) \
                        .filter(PlFixtures.finished == 0) \
                        .all())

def StillToPlayDetailed(session,gw,managedId,playerId):
    return len(session.query(Teams,Players,PlFixtures) \
                        .filter(Teams.playerId==Players.jfpl) \
                        .filter(or_(PlFixtures.away_team==Players.team,PlFixtures.home_team==Players.team)) \
                        .filter_by(managerId = managedId) \
                        .filter_by(gameweek = gw) \
                        .filter(Teams.playerId == playerId) \
                        .filter(PlFixtures.started == 0) \
                        .all())

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