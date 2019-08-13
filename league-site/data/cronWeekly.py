from methods import updatePlFixtures, updateGameweekPlayers,updateGameweeks,updateTeams,updatePlPlayers,updateChips,checkDrops,checkReefs
from models import CreateSession,Gameweeks
from dateutil import tz
import requests
import datetime
import time
from crontab import CronTab


def DateToCron()():
    session=CreateSession()
    q = session.query(Gameweeks) \
            .filter_by(is_next=1) \
            .first()
            
    dt = datetime.datetime.strptime(q.deadline,'%Y-%m-%dT%H:%M:%SZ')
    dt=dt.replace(tzinfo=tz.gettz('UTC'))
    return dt

def CreateWeeklyCronjob():
	cron = CronTab(user='turner_prize')
	job  = cron.new(command='/home/turner_prize/leagueolas/bot-env/bin/python3 /home/turner_prize/leagueolas/league-site/league-site/data/cronWeekly.py',comment='testcomment')
	dt = DateToCron()
	job.setall(dt)
	cron.write()



def DataAvailable():
    PC = requests.get("https://fantasy.premierleague.com/api/bootstrap-static")
    try:
        PC.json()
        return True
    except ValueError:
        return False

def WeeklySetup():
    updateGameweeks()
    updatePlFixtures
    updatePlPlayers()
    updateTeams()
    updateChips()
    checkDrops()
    checkReefs()
    CreateWeeklyCronjob()
    
while True:
	if DataAvailable():
		WeeklySetup()
		break
	else:
		sleep(120)


