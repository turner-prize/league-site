from config import ma,db
from models import DraftBoard,DraftedPlayers,Fixtures,Gameweeks,Managers,PLFixtures,PLTeams,Players,Table,TableHistory,Teams
from models import TH,FixturesReadable

class DraftBoardSchema(ma.ModelSchema):
    class Meta:
        model = DraftBoard
        sqla_session = db.session

class DraftedPlayersSchema(ma.ModelSchema):
    class Meta:
        model = DraftedPlayers
        sqla_session = db.session
        
class FixturesSchema(ma.ModelSchema):
    class Meta:
        model = Fixtures
        sqla_session = db.session

class GameweeksSchema(ma.ModelSchema):
    class Meta:
        model = Gameweeks
        sqla_session = db.session      

class ManagersSchema(ma.ModelSchema):
    class Meta:
        model = Managers
        sqla_session = db.session

class PLFixturesSchema(ma.ModelSchema):
    class Meta:
        model = PLFixtures
        sqla_session = db.session

class PLTeamsSchema(ma.ModelSchema):
    class Meta:
        model = PLTeams
        sqla_session = db.session

class PlayersSchema(ma.ModelSchema):
    class Meta:
        model = Players
        sqla_session = db.session

class TableSchema(ma.ModelSchema):
    class Meta:
        model = Table
        sqla_session = db.session

class TableHistorySchema(ma.ModelSchema):
    class Meta:
        model = TableHistory
        sqla_session = db.session

class TeamsSchema(ma.ModelSchema):
    class Meta:
        model = Teams
        sqla_session = db.session

#custom Schemas below

class THSchema(ma.ModelSchema):
    class Meta:
        model = TH
        sqla_session = db.session


#Ignore below, just a test for formatting queries to be consumable via API
class FixturesReadableSchema(ma.ModelSchema):
    class Meta:
        model = FixturesReadable
        sqla_session = db.session