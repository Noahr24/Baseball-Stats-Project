from flask import Blueprint, jsonify, request, url_for
from baseball_api.helpers import token_required
from baseball_api.models import Player, player_schema, players_schema, db

api = Blueprint('api', __name__, url_prefix='/api')


# This is for Creating the Player
@api.route('/players', methods = ['POST'])
@token_required
def create_player(current_user_token):
    name = request.json['name']
    team = request.json['team']
    position = request.json['position']
    user_token = current_user_token.token

    player = Player(name, team, position, user_token=user_token)

    db.session.add(player)
    db.session.commit()

    response = player_schema.dump(player)
    return jsonify(response)



# This is for retreveing multiple players
@api.route('/players', methods = ['GET'])
@token_required
def get_players(current_user_token):
    owner = current_user_token.token
    players = Player.query.filter_by(user_token = owner).all()
    response = players_schema.dump(players)
    return jsonify(response)


# This is for retreiving a player
@api.route('/players/<id>', methods = ['GET'])
@token_required
def get_player(current_user_token, id):
    player = Player.query.get(id)
    if player:
        response = player_schema.dump(player)
        return jsonify(response)
    else:
        return jsonify({'message': 'That player is not in our database'})


# This is for updating players
@api.route('/players/<id>', methods = ['POST'])
@token_required
def update_player(current_user_token, id):
    player = Player.query.get(id)
    if player:
        player.name = request.json['name']
        player.team = request.json['team']
        player.position = request.json['position']
        player.user_token = current_user_token.token

        db.session.commit()

        response = player_schema.dump(player)
        return jsonify(response)
    else:
        jsonify({'message': 'That player is not in our database'})


# This is for deleting players
@api.route('/players/<id>', methods = ['DELETE'])
@token_required
def delete_player(current_user_token, id):
    player = Player.query.get(id)
    if player:
        db.session.delete(player)
        db.session.commit()
        response = player_schema.dump(player)
        return jsonify(response)
    else:
        return jsonify({'message': 'That player is not in our database'})