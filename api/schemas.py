from config import ma,db
from models import DraftedPlayers, Fixtures, Managers,FixturesReadable,TableHistory,TH

class DraftedPlayersSchema(ma.ModelSchema):
    class Meta:
        model = DraftedPlayers
        sqla_session = db.session
        
        
class FixturesSchema(ma.ModelSchema):
    class Meta:
        model = Fixtures
        sqla_session = db.session
        
        
class ManagersSchema(ma.ModelSchema):
    class Meta:
        model = Managers
        sqla_session = db.session

class TableHistorySchema(ma.ModelSchema):
    class Meta:
        model = TableHistory
        sqla_session = db.session

class THSchema(ma.ModelSchema):
    class Meta:
        model = TH
        sqla_session = db.session


#Ignore below, just a test for formatting queries to be consumable via API
class FixturesReadableSchema(ma.ModelSchema):
    class Meta:
        model = FixturesReadable
        sqla_session = db.session