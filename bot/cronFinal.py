from methods import updatePlFixtures, updateGameweekPlayers,updateFixturesWithTablePoints,produceTable,createTable,updateTeamsFinalBench
from loguru import logger
from crontab import CronTab
import time
import requests

def clearCronjobs():
	cron = CronTab(user='turner_prize')

	for job in cron:
		if job.comment in ['Gameweek Match','Bonus Points','Final Points']:
			cron.remove(job)
	cron.write()

def setupLogger():
        logger.add('/home/turner_prize/leagueolas/league-site/league-site/data/cronFinal.log', format="{time} {level} {message}")


setupLogger()
logger.info('Starting Final Script')
while True:
    try:
        r = requests.get("https://fantasy.premierleague.com/api/event-status/")
        x=r.json()
        if x['leagues'] == 'Updated':
            logger.info('bonus added')
            updatePlFixtures()
            updateGameweekPlayers()
            updateTeamsFinalBench()
            updateFixturesWithTablePoints()
            produceTable()
            createTable()
            clearCronjobs()
            break
        else:
            logger.info('nothing yet')
            time.sleep(900)
    except Exception as e:
        logger.info('Error!')
        logger.info(e)
        break
logger.info('Final Update Completed')
