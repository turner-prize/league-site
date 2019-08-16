from methods import updatePlFixtures, updateGameweekPlayers,updateFixturesWithTablePoints,produceTable,createTable
import time
from loguru import logger


def setupLogger():
        logger.add('cronBonus.log', format="{time} {level} {message}")


setupLogger()
while True:
    try:
        r = requests.get("https://fantasy.premierleague.com/api/event-status/")
        x = r.json()
        for i in x['status']:
            if i['date'] == today:
                if i['bonus_added']:
                    logger.log('bonus added')
                    updatePlFixtures()
                    updateGameweekPlayers()
                    updateFixturesWithTablePoints()
                    produceTable()
                    createTable()
                    break
                else:
                    logger.log('nothing yet')
                    time.sleep(600)
    except Exception as e:
        logger.log('Error!')
        logger.log(e)
        break