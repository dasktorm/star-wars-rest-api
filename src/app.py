"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

with app.app_context():
    db.create_all()

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints

@app.route("/people", methods=["GET"])
def get_people():
    people = People.query.all()
    result = []
    for person in people:
        result.append({'id': person.id, 'name': person.name})
    return jsonify(result)

@app.route("/people/<int:people_id>", methods=["GET"])
def get_person(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify({'id': person.id, 'name': person.name})
    return jsonify({'error': 'People not found'}), 404

@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planets.query.all()
    result = []
    for planet in planets:
        result.append({'id': planet.id, 'name': planet.name})
    return jsonify(result)

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet:
        return jsonify({'id': planet.id, 'name': planet.name})
    return jsonify({'error': 'Planet not found'}), 404

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({'id': user.id, 'name': user.name})
    return jsonify(result)

@app.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    # Get the current user ID from the request or session
    user_id = request.args.get('user_id')
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    result = []
    for favorite in favorites:
        if favorite.planets_id:
            result.append({'planet_id': favorite.planets_id})
        elif favorite.people_id:
            result.append({'people_id': favorite.people_id})
    return jsonify(result)

@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    # Get the current user ID from the request or session
    user_id = request.args.get('user_id')
    favorite = Favorites(user_id=user_id, planets_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite planet added successfully'})

@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    # Get the current user ID from the request or session
    user_id = request.args.get('user_id')
    favorite = Favorites(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite people added successfully'})

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    # Get the current user ID from the request or session
    user_id = request.args.get('user_id')
    favorite = Favorites.query.filter_by(user_id=user_id, planets_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorite planet deleted successfully'})
    return jsonify({'error': 'Favorite planet not found'}), 404

@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(people_id):
    # Get the current user ID from the request or session
    user_id = request.args.get('user_id')
    favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorite people deleted successfully'})
    return jsonify({'error': 'Favorite people not found'}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)