from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import json
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
    
 
class tableSchema(ma.Schema):
    class Meta:
        fields = ('id','team','manager','points','playerScore')

table_schema = tableSchema(strict=True)
tables_schema = tableSchema(many=True, strict=True)
        
# endpoint to show all users
@app.route('/table', methods=['GET'])
def get_table():
  all_products = Table.query.all()
  result = tables_schema.dump(all_products)
  print(result.data)
  return jsonify(result.data)

    
if __name__ == '__main__':
    app.run(debug=True)