#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

def j_sonify(dict):
    response = make_response(jsonify(dict), 200)
    response.headers["Content-Type"] = "application/json"
    return response
    
class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        
        res = j_sonify(plants)
        return res
    
    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name = data['name'],
            image = data["image"],
            price = data["price"]
        )

        db.session.add(new_plant)
        db.session.commit()
        
        new_plant_dict = new_plant.to_dict()
        res = j_sonify(new_plant_dict)
        return res
        
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(int(id)).to_dict()
        
        res = j_sonify(plant)
        return res


api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
