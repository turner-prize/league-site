from models import CreateSession,PlFixtures
from methods import updatePlFixtures, updateGameweekPlayers
import time
import datetime
from dateutil import tz
from collections import namedtuple

def createCronJobs():
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
        KickoffTime=dt.astimezone(tz.tzlocal())
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

x=createCronJobs()
for i in x:
	print(i[1] - i[0])

#while True:
#    updatePlFixtures()
#    updateGameweekPlayers()
#    time.sleep(60)
