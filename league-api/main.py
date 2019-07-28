from flask import Flask, request, jsonify

from flask_cors import CORS
from models import Gameweeks,gameweekSchema, db, ma
import json
import random
import os

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'league.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)

gameweek_schema = gameweekSchema(strict=True)
gameweeks_schema = gameweekSchema(many=True, strict=True)
        
# endpoint to show all users
@app.route('/gameweeks', methods=['GET'])
def get_table():
  all_products = Gameweeks.query.filter_by(is_current='1').all()
  result = gameweeks_schema.dump(all_products)
  return jsonify(gw=result.data)
    
if __name__ == '__main__':
    app.run(debug=True)