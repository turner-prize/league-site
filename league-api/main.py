from flask import Flask, request, jsonify

from flask_cors import CORS
from models import Gameweeks,gameweekSchema, db, ma, Players,playerSchema, PlTeams, plTeamsSchema, Managers, managerSchema, DraftedPlayers, draftedPlayerSchema,DraftBoard, draftedBoardSchema
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

gameweeks_schema = gameweekSchema(many=True, strict=True)
players_schema = playerSchema(many=True, strict=True)
plTeams_schema = plTeamsSchema(many=True, strict=True)
managers_schema = managerSchema(many=True, strict=True)
draftboard_schema = draftedBoardSchema(many=True, strict=True)

# endpoint to show all users
@app.route('/gameweeks', methods=['GET'])
def get_table():
  all_products = Gameweeks.query.filter_by(is_current='1').all()
  result = gameweeks_schema.dump(all_products)
  return jsonify(gw=result.data)
  
@app.route('/managers', methods=['GET'])
def get_managers():
  all_products = Managers.query.order_by(Managers.draftPick.asc()).all()
  result = managers_schema.dump(all_products)
  return jsonify(result.data)
  
@app.route('/players', methods=['GET'])
def get_players():
  all_Players = Players.query.join(PlTeams) \
                .add_columns(
                              Players.jfpl,
                              Players.first_name,
                              Players.second_name,
                              Players.element_type,
                              Players.drafted,
                              PlTeams.shortname,
                              PlTeams.name).filter(Players.drafted==0).all()
  result = players_schema.dump(all_Players)
  return jsonify(result.data)

@app.route('/draftplayers', methods=['POST'])
def recieve_players():
  if request.method == 'POST':
    response = request.get_json()
    managerid = response['Manager']['teamId']
    draftPlayers(managerid,response['GK']['id'])
    draftPlayers(managerid,response['DF1']['id'])
    draftPlayers(managerid,response['DF2']['id'])
    draftPlayers(managerid,response['MF1']['id'])
    draftPlayers(managerid,response['MF2']['id'])
    draftPlayers(managerid,response['FWD']['id'])
  return 'this worked'

@app.route('/draftboard', methods=['GET'])
def get_draftboard():
  all_Players = DraftBoard.query.join(Managers) \
                .add_columns(
                              Managers.id,
                              Managers.draftPick,
                              Managers.teamName,
                              DraftBoard.GK,
                              DraftBoard.DF1,
                              DraftBoard.DF2,
                              DraftBoard.MF1,
                              DraftBoard.MF2,
                              DraftBoard.FWD).order_by(Managers.draftPick.asc()).all()
  result = draftboard_schema.dump(all_Players)
  return jsonify(result.data)

def draftPlayers(managerid,playerid):
    dp = DraftedPlayers(managerId=managerid,playerId=playerid)
    db.session.add(dp)
    player = Players.query.filter_by(jfpl=playerid).first()
    player.drafted = 1
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)