from models import CreateSession,PlFixtures,Players
from methods import updatePlFixtures, updateGameweekPlayers,updateFixturesWithTablePoints,produceTable,createTable
import time
from datetime import datetime, timedelta
from dateutil import tz
from collections import namedtuple
from loguru import logger

def GetFixtures():
    session=CreateSession()
    q = session.query(PlFixtures.kickoff_time) \
        .distinct(PlFixtures.kickoff_time) \
        .order_by(PlFixtures.kickoff_time) \
        .all()
    dtRanges=[]
    for i in q:
        #timezone is UTC from database, need to change to current TZ
        KickoffTime = datetime.strptime(i.kickoff_time,'%Y-%m-%dT%H:%M:%SZ')
        GameEndTime=KickoffTime + timedelta(hours=2)
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

def setupLogger():
        logger.add('cronlog.log', format="{time} {level} {message}")

def getRangeNumber():
    x=GetFixtures()
    y = min([abs(i[0] - datetime.utcnow()) for i in x])
    z = {abs(i[0] - datetime.utcnow()):i[0] for i in x}


    for i in x:
        if i[0] == z[y]:
            myDifference = i[1] - i[0]
            timer = myDifference.seconds / 120
            
    return timer

#If regular game, do until just past full time.

#if last game of day, do untiMl bonus is added. If i[0].day == today(), when time limit is up, check bonus and sleep(600). 
#r = requests.get("https://fantasy.premierleague.com/api/event-status/")
#x = r.json()
#for i in x['status']:
#	if i['date'] == today:
#		if i['bonus_added']:
#

#If last game of week, do until league is updated, and then run 'updateteamsfinalbench' from methods.
#r = requests.get("https://fantasy.premierleague.com/api/event-status/")
#x=r.json()
#if x['leagues'] == 'Updated'

#in both last game of day/week, past full time drop the fetching to every 15 minutes.


setupLogger()
for i in range(getRangeNumber()):
    try:
        updatePlFixtures()
        updateGameweekPlayers()
        updateFixturesWithTablePoints()
        produceTable()
        createTable()
        time.sleep(120)
    except Exception as e:
        logger.log('Error!')
        logger.log(e)
        break
