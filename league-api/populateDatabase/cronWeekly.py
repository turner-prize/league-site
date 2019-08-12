from methods import updatePlFixtures, updateGameweekPlayers,updateGameweeks,updateTeams,updatePlPlayers
import requests
import time


def DataAvailable():
    PC = requests.get("https://fantasy.premierleague.com/drf/bootstrap")
    try:
        PC.json()
        return True
    except ValueError:
        return False

def WeeklySetup():
    updateGameweeks()
    updatePlPlayers()
    updateTeams()
    updateChips()
    checkDrops()
    checkReefs()
    
    
while True:
    if DataAvailable():
        WeeklySetup()
        break
    else:
        sleep(300)

