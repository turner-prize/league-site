from methods import updatePlFixtures, updateGameweekPlayers,updateGameweeks,updateTeams,updatePlPlayers,updateChips,checkDrops,checkReefs
from models import CreateSession,Gameweeks,PlFixtures
from dateutil import tz
import requests
import datetime
import time
from crontab import CronTab
from collections import namedtuple
from loguru import logger

def getKickoffTimes():
    session=CreateSession()
    q = session.query(PlFixtures.kickoff_time) \
            .distinct(PlFixtures.kickoff_time) \
            .order_by(PlFixtures.kickoff_time) \
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
    q = session.query(PlFixtures.kickoff_time).all()
    gameDays = set([datetime.strptime(i[0],'%Y-%m-%dT%H:%M:%SZ').date() for i in q])
    for i in gameDays:
        KO = max([datetime.strptime(j[0],'%Y-%m-%dT%H:%M:%SZ') for j in q if datetime.strptime(j[0],'%Y-%m-%dT%H:%M:%SZ').date() == i])
        FT = KO + timedelta(hours=2)
        job  = cron.new(command='/home/turner_prize/leagueolas/bot-env/bin/python3 /home/turner_prize/leagueolas/league-site/league-site/data/cronBonus.py',comment='Gameweek Match')
        job.setall(FT)
		cron.write()
    session.close()

def CreateFinalCronjobs():
    cron = CronTab(user='turner_prize')
    session=CreateSession()
    q = session.query(PlFixtures.kickoff_time).all()
    KO = max([datetime.strptime(j[0],'%Y-%m-%dT%H:%M:%SZ') for j in q])
    FT = KO + timedelta(hours=2)
    job  = cron.new(command='/home/turner_prize/leagueolas/bot-env/bin/python3 /home/turner_prize/leagueolas/league-site/league-site/data/cronFinal.py',comment='Gameweek Match')
    job.setall(FT)
    cron.write()
    session.close()

def DataAvailable():
    PC = requests.get("https://fantasy.premierleague.com/api/bootstrap-static")
    try:
        PC.json()
        return True
    except ValueError:
        return False

def setupLogger():
	logger.add('cronWeekly.log', format="{time} {level} {message}")

def WeeklySetup():
    updateGameweeks()
    updatePlFixtures
    updatePlPlayers()
    updateTeams()
    updateChips()
    checkDrops()
    checkReefs()
    CreateMatchCronJobs()
    CreateWeeklyCronjob()
    

if __name__ == "__main__":
	setupLogger()
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
	
