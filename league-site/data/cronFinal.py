from methods import updatePlFixtures, updateGameweekPlayers,updateFixturesWithTablePoints,produceTable,createTable
import time
from loguru import logger


def setupLogger():
        logger.add('cronFinal.log', format="{time} {level} {message}")


setupLogger()
while True:
    try:
        r = requests.get("https://fantasy.premierleague.com/api/event-status/")
        x=r.json()
        if x['leagues'] == 'Updated'
            logger.log('bonus added')
            updatePlFixtures()
            updateGameweekPlayers()
            updateFixturesWithTablePoints()
            produceTable()
            createTable()
            break
        else:
            logger.log('nothing yet')
            time.sleep(900)
    except Exception as e:
        logger.log('Error!')
        logger.log(e)
        break