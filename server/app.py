#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

# Setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize DB and migrations
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Flask-RESTful API
api = Api(app)

@app.route('/')
def index():
    return '<h1>Code Challenge</h1>'


# Resource for handling Heroes
class HeroListResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
        return jsonify(heroes_data)


class HeroResource(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if hero:
            hero_data = {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name,
                'hero_powers': [{
                    'hero_id': hp.hero_id,
                    'id': hp.id,
                    'strength': hp.strength,
                    'power': {
                        'id': hp.power.id,
                        'name': hp.power.name,
                        'description': hp.power.description
                    }
                } for hp in hero.hero_powers]
            }
            return jsonify(hero_data)
        else:
            return make_response(jsonify({"error": "Hero not found"}), 404)


# Resource for handling Powers
class PowerListResource(Resource):
    def get(self):
        powers = Power.query.all()
        powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
        return jsonify(powers_data)


class PowerResource(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if power:
            power_data = {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }
            return jsonify(power_data)
        else:
            return make_response(jsonify({"error": "Power not found"}), 404)

    def patch(self, id):
        power = Power.query.get(id)
        if not power:
            return make_response(jsonify({"error": "Power not found"}), 404)
        
        data = request.get_json()
        try:
            if 'description' in data and len(data['description']) >= 20:
                power.description = data['description']
                db.session.commit()
                return jsonify({
                    'id': power.id,
                    'name': power.name,
                    'description': power.description
                })
            else:
                raise ValueError("Description must be at least 20 characters long.")
        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)


# Resource for handling HeroPower
class HeroPowerResource(Resource):
    def post(self):
        # Check if Content-Type is application/json
        if request.content_type != 'application/json':
            return make_response(jsonify({"error": "Content-Type must be application/json"}), 400)
        
        # Parse JSON data
        data = request.get_json()

        # Validate 'strength' field
        if data.get('strength') not in ['Strong', 'Weak', 'Average']:
            return make_response(jsonify({"errors": ["Strength must be 'Strong', 'Weak', or 'Average'."]}), 400)

        # Validate if hero_id and power_id exist
        hero = Hero.query.get(data.get('hero_id'))
        power = Power.query.get(data.get('power_id'))

        if not hero:
            return make_response(jsonify({"error": "Hero not found"}), 404)
        if not power:
            return make_response(jsonify({"error": "Power not found"}), 404)

        try:
            # Create a new HeroPower
            new_hero_power = HeroPower(
                strength=data['strength'],
                hero_id=data['hero_id'],
                power_id=data['power_id']
            )
            db.session.add(new_hero_power)
            db.session.commit()

            # Prepare the response with the new HeroPower data
            hero_power_data = {
                'id': new_hero_power.id,
                'hero_id': new_hero_power.hero_id,
                'power_id': new_hero_power.power_id,
                'strength': new_hero_power.strength,
                'hero': {
                    'id': new_hero_power.hero.id,
                    'name': new_hero_power.hero.name,
                    'super_name': new_hero_power.hero.super_name
                },
                'power': {
                    'id': new_hero_power.power.id,
                    'name': new_hero_power.power.name,
                    'description': new_hero_power.power.description
                }
            }
            return jsonify(hero_power_data), 201
        except Exception as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)


# Register API Resources with Routes
api.add_resource(HeroListResource, '/heroes')
api.add_resource(HeroResource, '/heroes/<int:id>')
api.add_resource(PowerListResource, '/powers')
api.add_resource(PowerResource, '/powers/<int:id>')
api.add_resource(HeroPowerResource, '/hero_powers')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
