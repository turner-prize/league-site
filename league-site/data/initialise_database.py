from methods import GetBootstrapData,GetGameweek
from models import CreateSession, Gameweeks


def populateGameweeks():
    bootstrapData = GetBootstrapData()
    gameweekData = bootstrapData['events']
    session=CreateSession()
    for i in gameweekData:
        gw = Gameweeks( id=i['id'],
                        name=i['name'],
                        deadline=i['deadline_time'],
                        is_current=i['is_current'],
                        is_next=i['is_next'],
                        gameweek_start='test',
                        gameweek_end='test')
        session.add(gw)
        session.commit()
    session.close()

#method to initialise the Premier League Players in the database.
def populatePlayers():
    bootstrapData = GetBootstrapData()
    playerData = bootstrapData['elements']
    session=CreateSession()
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

#method to initialise the Fixtures table in the database. Possibly defunct if we use our own site, as we can create our own fixtures.
def populateFixtures(): 
    for i in range(1,5):
        r = requests.get(f"https://fantasy.premierleague.com/api/leagues-h2h-matches/league/326910/?page={i}")
        data = r.json()
        fixtureData = data['results']
        
        session=CreateSession()
        
        for f in fixtureData:
            teamfplid = f['entry_1_entry']
            opponentId = f['entry_2_entry']
            m = session.query(Managers).filter_by(fplId=teamfplid).first()
            o = session.query(Managers).filter_by(fplId=opponentId).first()
            fxtr = Fixtures(gameweek = f['event'],
                            managerId = m.id,
                            opponentId = o.id)
            rvrsfxtr = Fixtures(gameweek = f['event'],
                            managerId = o.id,
                            opponentId = m.id)
            session.add(fxtr)
            session.add(rvrsfxtr)
        session.commit()
        session.close()
        
        
#method to initialise the Premier League Teams in the database.
def populatePlTeams():
    bootstrapData = GetBootstrapData()
    plTeamsData = bootstrapData['teams']
    session=CreateSession()
    for i in plTeamsData:
        tm = PlTeams(   id = i['id'],
                        name = i['name'],
                        shortname = i['short_name'])
        session.add(tm)
        session.commit()
    session.close()
    
#method to initialise the Premier League Fxitures in the database.
def populatePlFixtures():
    session=CreateSession()
    gw = GetGameweek()
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