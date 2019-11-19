from methods import getNewPlFixtures, updateGameweekPlayers,updateGameweeks,updateTeams,updatePlPlayers,updateChips,checkDrops,checkReefs
from models import CreateSession,Gameweeks,PlFixtures
from dateutil import tz
import requests
import datetime
import time
from crontab import CronTab
from collections import namedtuple
from loguru import logger

def GetGameweek(session):
    gw = session.query(Gameweeks.id).filter_by(is_current=1).first()
    return gw[0]

def getKickoffTimes():
    session=CreateSession()
    gw=GetGameweek(session)
    q = session.query(PlFixtures.kickoff_time) \
            .distinct(PlFixtures.kickoff_time) \
            .order_by(PlFixtures.kickoff_time) \
            .filter_by(gameweek=gw) \
            .all()
    dtRanges=[]
    for i in q:
        #timezone is UTC from database, need to change to current TZ
        dt = datetime.datetime.strptime(i.kickoff_time,'%Y-%m-%dT%H:%M:%SZ')
        dt=dt.replace(tzinfo=tz.gettz('UTC'))
        KickoffTime=dt
        GameEndTime=KickoffTime + datetime.timedelta(hours=2)
        rng = (KickoffTime,GameEndTime)
        dtRanges.append(rng)
    session.close()
    return LoopIt(dtRanges)

def LoopIt(rng):
    Range = namedtuple('Range', ['start', 'end'])
    for i,val in enumerate(rng):
        try:
            r1 = Range(start=val[0], end=val[1])
            r2 = Range(start=rng[i+1][0], end=rng[i+1][1])
            latest_start = max(r1.start, r2.start)
            earliest_end = min(r1.end, r2.end)
            delta = (earliest_end - latest_start).days + 1
            overlap = max(0, delta)
            if overlap==0:
                pass
            else:
                newRng = (val[0],rng[i+1][1])
                rng[i] = newRng
                rng.pop(i+1)
                LoopIt(rng)
        except IndexError:
            pass
    return rng

def DateToCron():
    session=CreateSession()
    q = session.query(Gameweeks) \
            .filter_by(is_next=1) \
            .first()
            
    dt = datetime.datetime.strptime(q.deadline,'%Y-%m-%dT%H:%M:%SZ')
    dt=dt.replace(tzinfo=tz.gettz('UTC'))
    return dt

def CreateWeeklyCronjob():
	cron = CronTab(user='turner_prize')
	job  = cron.new(command='/home/turner_prize/leagueolas/bot-env/bin/python3 /home/turner_prize/leagueolas/league-site/league-site/data/cronWeekly.py')
	dt = DateToCron()
	job.setall(dt)
	cron.write()

def CreateMatchCronjobs():
	cron = CronTab(user='turner_prize')
	for i in getKickoffTimes():
		job  = cron.new(command='/home/turner_prize/leagueolas/bot-env/bin/python3 /home/turner_prize/leagueolas/league-site/league-site/data/cron.py',comment='Gameweek Match')
		job.setall(i[0])
		cron.write()

def CreateBonusCronjobs():
    cron = CronTab(user='turner_prize')
    session=CreateSession()
    gw=GetGameweek(session)
    q = session.query(PlFixtures.kickoff_time).filter_by(gameweek=gw).all()
    gameDays = set([datetime.datetime.strptime(i[0],'%Y-%m-%dT%H:%M:%SZ').date() for i in q])
    for i in gameDays:
        KO = max([datetime.datetime.strptime(j[0],'%Y-%m-%dT%H:%M:%SZ') for j in q if datetime.datetime.strptime(j[0],'%Y-%m-%dT%H:%M:%SZ').date() == i])
        FT = KO + datetime.timedelta(hours=2)
        job  = cron.new(command='/home/turner_prize/leagueolas/bot-env/bin/python3 /home/turner_prize/leagueolas/league-site/league-site/data/cronBonus.py',comment='Bonus Points')
        job.setall(FT)
        cron.write()
    session.close()

def CreateFinalCronjobs():
    cron = CronTab(user='turner_prize')
    session=CreateSession()
    gw=GetGameweek(session)
    q = session.query(PlFixtures.kickoff_time).filter_by(gameweek=gw).all()
    KO = max([datetime.datetime.strptime(j[0],'%Y-%m-%dT%H:%M:%SZ') for j in q])
    FT = KO + datetime.timedelta(hours=2)
    job  = cron.new(command='/home/turner_prize/leagueolas/bot-env/bin/python3 /home/turner_prize/leagueolas/league-site/league-site/data/cronFinal.py',comment='Final Points')
    job.setall(FT)
    cron.write()
    session.close()

def DataAvailable():
    PC = requests.get("https://fantasy.premierleague.com/api/event-status/")
    try:
        if PC.json() == "The game is being updated.":
            return False
        else:
            return True
    except ValueError:
        return False

def setupLogger():
	logger.add('/home/turner_prize/leagueolas/league-site/league-site/data/cronWeekly.log', format="{time} {level} {message}")

def WeeklySetup():
    updateGameweeks()
    logger.info('gameweeks updated')
    getNewPlFixtures()
    logger.info('plfixtures updated')
    updatePlPlayers()
    logger.info('plplayers updated')
    updateTeams()
    logger.info('Teams updated')
    updateChips()
    logger.info('chips updated')
    checkDrops()
    logger.info('drops updated')
    checkReefs()
    logger.info('reefs updated')
    CreateMatchCronjobs()
    CreateWeeklyCronjob()
    CreateBonusCronjobs()
    CreateFinalCronjobs()    

if __name__ == "__main__":
    setupLogger()
    logger.info('sleeping for 5 minutes to not fuck things up')
    time.sleep(300)
    while True:
        try:
            logger.info('trying to access api')
            if DataAvailable():
                logger.info('success! running weekly setup')
                WeeklySetup()
                break
            else:
                logger.info('not available, sleeping for 2 minutes')
                time.sleep(120)
        except Exception as e:
            logger.info('Error:')
            logger.info(e)
            break
	
