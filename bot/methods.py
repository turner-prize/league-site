from models import Gameweeks, CreateSession, Managers, Teams,Players,DraftedPlayers, Fixtures, PlFixtures, Table
from sqlalchemy import update, Integer, desc
from sqlalchemy.orm import aliased,sessionmaker
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas
import numpy as np
import matplotlib.pyplot as plt
import six
import os
import telegram
from btoken import BotToken

def sendMsg(msg):
    chats =     [282457851,
                 423370337,
                 331801993,
                 408778637,
                 346959464,
                 392414867,
                 404362781,
                 420101994,
                 420261096,
                 402233322,
                 668999191]
    bot = telegram.Bot(token=BotToken)
    for i in chats:
        try:
            bot.send_message(chat_id=i, text=msg)
        except:
            print(i)
            pass



def render_mpl_table(data,filename, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in  six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    fig.savefig(filename)
    return ax

def createTable():
    session=CreateSession()
    t = session.query(Table,Managers).filter(Table.managerId == Managers.id).all()
    values = [(i[1].teamName,i[0].score,i[0].points) for i in t]
    session.close()
    df = pandas.DataFrame(values, columns = ['Team' , 'PlayerScore', 'Points'])
    df = df.sort_values(['Points','PlayerScore'], ascending=[False, False])
    df = df.reset_index()
    df.drop('index', axis=1, inplace=True)
    df['#'] = df.index +1
    df['#'] = df['#'].apply(lambda x: "{}{}".format(x, (' '*15) ))
    df = df[['#','Team', 'PlayerScore', 'Points']]
    render_mpl_table(df,'/home/turner_prize/leagueolas/league-site/league-site/data/table.png')

def TripleCaptain(session,managerId,gw):
    TC = session.query(Managers).filter_by(id=managerId).filter_by(TC=gw).first()
    return TC

def produceTable():
    session=CreateSession()
    p = session.query(Table).delete()
    session.commit()
    managers = session.query(Managers).all()
    for m in managers:
        f = session.query(Fixtures).filter_by(managerId=m.id).all()
        score = sum([i.score for i in f if i.score is not None])
        points = sum([i.points for i in f if i.score is not None])
        tb = Table(managerId=m.id,
                    score=score,
                    points=points)
        session.add(tb)
    session.commit()
    t = session.query(Table).order_by(desc(Table.points)).order_by(desc(Table.score)).all()
    p = session.query(Table).delete()
    session.commit()
    x = 0
    for i in t:
        x += 1
        tb = Table(position=x,
                    managerId=i.managerId,
                    score=i.score,
                    points=i.points)
        session.add(tb)
    session.commit()
    session.close()

def updateFixturesWithTablePoints():
    session=CreateSession()
    gw = GetGameweek(session)
    fixtures = session.query(Fixtures).filter_by(gameweek=gw).all()
    for f in fixtures:
        scores = session.query(Teams).filter_by(managerId=f.managerId).filter_by(gameweek=gw).filter_by(is_bench=0).all()
        scoreList = []
        for i in scores:
            if i.is_captain==1:
                if TripleCaptain(session,f.managerId,gw):
                    scoreList.append(i.points * 3)
                else:
                    scoreList.append(i.points * 2)
            else:
                scoreList.append(i.points)
        points = sum(scoreList)
        scoresOpponent = session.query(Teams).filter_by(managerId=f.opponentId).filter_by(gameweek=gw).filter_by(is_bench=0).all()
        scoreOpponentList = []
        for i in scoresOpponent:
            if i.is_captain==1:
                if TripleCaptain(session,f.managerId,gw):
                    scoreOpponentList.append(i.points * 3)
                else:
                    scoreOpponentList.append(i.points * 2)
            else:
                scoreOpponentList.append(i.points)
        pointsOpponent = sum(scoreOpponentList)
        
        f.score = points
        if points > pointsOpponent:
            f.points = 3
        elif points == pointsOpponent:
            f.points = 1
        else:
            f.points = 0
        session.add(f)
        session.commit()
    session.close()

def getNewPlFixtures():
    session=CreateSession()
    gw = GetGameweek(session)
    r = requests.get(f"https://fantasy.premierleague.com/api/fixtures/?event={gw}")
    fixtureData = r.json()
    for i in fixtureData:
        fxtr = PlFixtures(  id = i['id'],
                            kickoff_time = i['kickoff_time'],
                            gameweek = i['event'],
                            away_team = i['team_a'],
                            home_team = i['team_h'],
                            started = i['started'],
                            finished = i['finished'])
        session.add(fxtr)
        session.commit()
    session.close()

def updatePlFixtures():
    session=CreateSession()
    gw = GetGameweek(session)
    r = requests.get(f"https://fantasy.premierleague.com/api/fixtures/?event={gw}")
    fixtureData = r.json()
    for games in fixtureData:
        j = session.query(PlFixtures).filter_by(away_team=games['team_a']).filter_by(gameweek=gw).first()
        if games['started']:
            j.started = 1
        if games['finished_provisional']:
            j.finished = 1
        session.add(j)
    session.commit()
    session.close()


def reefed(session,managerId,playerId,gw):
    reefed = session.query(Teams.reefed).filter_by(managerId=managerId).filter_by(playerId=playerId).filter_by(gameweek=gw).first()
    return reefed[0]

def updateTeamsFinalBench():
    session=CreateSession()
    m = session.query(Managers).all()
    gw = GetGameweek(session)
    for i in m:
        fplid = i.fplId
        r = requests.get(f"https://fantasy.premierleague.com/api/entry/{fplid}/event/{gw}/picks/")
        team = r.json()
        for p in team['picks']:
            if p['is_captain']:
                cap = 1
            else:
                cap = 0
            if not BenchBoost(session,i.id,gw):
                if p['position']> 11:
                    bench = 1
                else:
                    bench = 0
            else:
                bench = 0
            plyr = session.query(Teams).filter_by(playerId=p['element']).filter_by(managerId=i.id).filter_by(gameweek=gw).first()
            plyr.is_bench = bench
            session.add(plyr)
    session.commit()
    session.close()

def updateGameweekPlayers():
    session=CreateSession()
    gw = GetGameweek(session)
    players = session.query(Teams.playerId).filter_by(gameweek=gw).all()
    players = {p[0] for p in players}
    urls = [f"https://fantasy.premierleague.com/api/element-summary/{i}/" for i in players]
    pool = ThreadPoolExecutor(len(urls))
    futures = [pool.submit(requests.get,url) for url in urls]
    results = [r.result() for r in as_completed(futures)]
    for r in results:
        player = r.json() #this can be cleaned up but it works for now
        for x in player['history']:
            if x['round'] == gw:
                for i in players:
                    if x['element'] == i:
                        playerName = session.query(Players.web_name).filter_by(jfpl=i).first()
                        myscore = int(x['total_points'])
                        #j = update(Teams).where(Teams.playerId==i).values(points=myscore)
                        j = session.query(Teams).filter_by(playerId=i).filter_by(gameweek=gw).all()
                        for entries in j:
                            h = entries
                            if reefed(session,entries.managerId,entries.playerId,entries.gameweek):
                                h.points = - myscore
                            else:
                                h.points = myscore
                            session.add(h)
    session.commit()
    session.close()

def checkReefs():
    session=CreateSession()
    gw = GetGameweek(session)
    drafted = session.query(DraftedPlayers).all()
    managers = session.query(Managers).all()
    
    for m in managers:
        thisWeeksTeams = session.query(Teams).filter(Teams.managerId == m.id).filter_by(gameweek=gw).all()
        thisWeeksTeams = [p.playerId for p in thisWeeksTeams]
        drafted = session.query(DraftedPlayers).filter(DraftedPlayers.managerId != m.id).all()
        drafted = [p.playerId for p in drafted]
        for d in drafted:
            if d in thisWeeksTeams:
                playerName = session.query(Players.web_name).filter_by(jfpl=d).first()
                managerName = m.name                
                reefedFrom = session.query(DraftedPlayers.managerId).filter_by(playerId=d).first()
                reefedFrom = session.query(Managers.name).filter_by(id=reefedFrom[0]).first()
                reefString = f'{managerName} has reefed {playerName[0]} from {reefedFrom[0]}'
                sendMsg(reefString)
                r = session.query(Teams).filter(Teams.managerId == m.id).filter_by(playerId = d).filter_by(gameweek=gw).first()
                r.reefed = 1
                session.add(r)
    session.commit()
    session.close()
    
def checkDrops():
    session=CreateSession()
    gw = GetGameweek(session)
    drafted = session.query(DraftedPlayers).all()
    
    for d in drafted:
        thisWeeksTeams = session.query(Teams).filter_by(gameweek=gw).filter_by(managerId=d.managerId).all()
        teamList = [x.playerId for x in thisWeeksTeams]
        if d.playerId not in teamList:
            playerName = session.query(Players.web_name).filter_by(jfpl=d.playerId).first()
            managerName = session.query(Managers.name).filter_by(id=d.managerId).first()
            dropString = f'{playerName[0]} has been dropped by {managerName[0]}'
            sendMsg(dropString)
            #delete players from draftlist
            p = session.query(DraftedPlayers).filter_by(playerId=d.playerId).delete()
    session.commit()
    session.close()
    

def updateChips():
    session=CreateSession()
    m = session.query(Managers).all()
    gw = GetGameweek(session)
    for i in m:
        fplid = i.fplId
        r = requests.get(f"https://fantasy.premierleague.com/api/entry/{fplid}/event/{gw}/picks/")
        team = r.json()
        if team['active_chip'] != 'null':
            if team['active_chip'] == '3xc':
                i.TC = gw
            if team['active_chip'] == 'bboost':
                i.BB = gw
            if team['active_chip'] == 'freehit':
                i.FH = gw
            if team['active_chip'] == 'wildcard':
                i.WC1 = gw
            
    session.commit()
    session.close()


def updatePlPlayers():
    session=CreateSession()
    p = session.query(Players).delete()
    bootstrapData = GetBootstrapData()
    playerData = bootstrapData['elements']
    for i in playerData:
        plyr = Players( jfpl = i['id'],
                        event_points = i['event_points'],
                        first_name = i['first_name'],
                        second_name = i['second_name'],
                        web_name= i['web_name'],
                        team = i['team'],
                        team_code = i['team_code'],
                        goals_scored = i['goals_scored'],
                        assists = i['assists'],
                        goals_conceded = i['goals_conceded'],
                        pen_saved = i['penalties_saved'],
                        pen_missed = i['penalties_missed'],
                        yellow_cards = i['yellow_cards'],
                        red_cards = i['red_cards'],
                        saves = i['saves'],
                        element_type = i['element_type'])
        session.add(plyr)
    session.commit()
    session.close()

def BenchBoost(session,managerId,gw):
    BB = session.query(Managers).filter_by(id=managerId).filter_by(BB=gw).first()
    return BB


def updateTeams():
    session=CreateSession()
    m = session.query(Managers).all()
    gw = GetGameweek(session)
    for i in m:
        fplid = i.fplId
        r = requests.get(f"https://fantasy.premierleague.com/api/entry/{fplid}/event/{gw}/picks/")
        team = r.json()
        for p in team['picks']:
            if p['is_captain']:
                cap = 1
            else:
                cap = 0
            if not BenchBoost(session,i.id,gw):
                if p['position']> 11:
                    bench = 1
                else:
                    bench = 0
            else:
                bench = 0
            plyr = Teams(gameweek=gw,
                        managerId=i.id,
                        playerId=int(p['element']),
                        points=0,
                        is_captain=cap,
                        is_bench=bench)
            session.add(plyr)
    session.commit()
    session.close()

                        

def updateGameweeks():
    bootstrapData = GetBootstrapData()
    gameweekData = bootstrapData['events']
    for i in gameweekData:
        if i['is_current']:
            thisWeek = i['id']
            if thisWeek < 38:
                nextWeek = thisWeek + 1
            break
            
    session=CreateSession()
    
    resetGameweeks(session)
    tw = session.query(Gameweeks).filter_by(id=thisWeek).first()
    tw.is_current = 1
    session.add(tw)
    if nextWeek:
        nw = session.query(Gameweeks).filter_by(id=nextWeek).first()
        nw.is_next = 1
        session.add(nw)
    session.commit()
    session.close()

def GetBootstrapData():
    r = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    return r.json()

def GetGameweek(session):
    gw = session.query(Gameweeks.id).filter_by(is_current=1).first()
    return gw[0]

def resetGameweeks(session):
    tw = session.query(Gameweeks).all()
    for i in tw:
        i.is_current = 0
        i.is_next = 0
        session.add(i)