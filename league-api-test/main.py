from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import json
import random
import os

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'league.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer,primary_key=True)
    team = db.Column(db.String(50))
    manager = db.Column(db.String(50))
    points = db.Column(db.Integer)
    playerScore = db.Column(db.Integer)
    
    def __init__(self,team,points,playerScore):
        self.team = team
        self.points = points
        self.playerScore = playerScore
        
class TableHistory(db.Model):
    __tablename__ = 'tableHistory'
    id = db.Column(db.Integer,primary_key=True)
    gameweek = db.Column(db.Integer)
    manager = db.Column(db.String(50))
    position = db.Column(db.Integer)
    
    def __init__(self,gameweek,manager,position):
        self.gameweek = gameweek
        self.manager = manager
        self.position = position
    
 
class tableSchema(ma.Schema):
    class Meta:
        fields = ('id','team','manager','points','playerScore')
        
class tableHistorySchema(ma.Schema):
    class Meta:
        fields = ('id','gameweek','manager','position')

table_schema = tableSchema(strict=True)
tables_schema = tableSchema(many=True, strict=True)
table_history_schema = tableHistorySchema(strict=True)
tables_history_schema = tableHistorySchema(many=True, strict=True)
        
# endpoint to show all users
@app.route('/table', methods=['GET'])
def get_table():
  all_products = Table.query.all()
  result = tables_schema.dump(all_products)
  return jsonify(result.data)

@app.route('/tablehistory', methods=['GET'])
def get_table_history():
  all_products = TableHistory.query.all()
  managers =list(set([i.manager for i in all_products]))
  managers = [{'label':i} for i in managers]
  for m in managers:
      pos = []  
      for i in all_products:
        if i.manager == m['label']:
            pos.append(i.position)
      m['data'] = pos
      m['fill'] = False
      r = lambda: random.randint(0,255)
      m['backgroundColor'] = '#%02X%02X%02X' % (r(),r(),r())
      
  return jsonify(datasets=managers,labels=[1,2,3])
    
if __name__ == '__main__':
    app.run(debug=True)