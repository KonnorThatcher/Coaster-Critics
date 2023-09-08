"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Park, Coaster
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/parks', methods=['GET'])
def get_all_parks():
    parks = Park.query.all()

    return jsonify(
        parks=[park.serialize() for park in parks]
    ), 200

@api.route('/parks', methods=['POST'])
def add_park():
    '''
    Konnor's Note: I used ChatGPT to generate this JSON File. If you do it that way, make sure to check for any typos
    and that it is formated correctly based on the below example.

    POST 
    {
        "park": {
            "name": "Kings Island",         <-- string
            "location": "Mason, Ohio, USA", <-- string
            "year_opened": 1972,            <-- string
            "coasters": [
                {
                  "name": "Adventure Express",          <-- string
                  "ride_type": "Mine train coaster",    <-- string
                  "height": "50 feet",                  <-- string
                  "track_length": "1,150 feet",         <-- string
                  "max_speed": "35 mph",                <-- string
                  "manufacturer": "Arrow Dynamics",     <-- string
                  "year_opened": 1991,                  <-- integer
                  "inversions": 0,                      <-- integer
                  "tallest_drop": "42 feet",            <-- string
                  "drop_angle": "50 degrees"            <-- string
                },
                ...
            ]
        }
    }
    '''
    park = request.json['park']

    the_same_park = Park.query.filter_by(name=park['name'], location=park["location"]).first()
    if the_same_park:
        return jsonify("This park is already in our database"), 400
        
    db.session.merge(Park(
        name=park['name'],
        location=park['location'],
        year_opened=park['year_opened']
    ))
    db.session.commit()
    park_id = Park.query.filter_by(name=park["name"], location=park["location"]).first().id

    for coaster in park['coasters']:
        db.session.merge(Coaster(
            name=coaster["name"],
            year_opened=coaster["year_opened"],
            park_id=park_id,
            ride_type=coaster["ride_type"],
            manufacturer=coaster["manufacturer"],
            track_length=coaster["track_length"],
            height=coaster["height"],
            tallest_drop=coaster["tallest_drop"],
            drop_angle=coaster["drop_angle"],
            max_speed=coaster["max_speed"],
            inversions=coaster["inversions"]
        ))
    db.session.commit()

    return jsonify("Park successfully merged!"), 204

@api.route('/parks/<int:id>', methods=['GET'])
def get_park(id):
    park = Park.query.filter_by(id=id).first()

    return jsonify(park.serialize()), 200

@api.route('/coasters', methods=['GET'])
def get_all_coasters():
    coasters = Coaster.query.all()

    return jsonify(
        coasters=[coaster.serialize() for coaster in coasters]
    ), 200

@api.route('/coasters', methods=['POST'])
def add_coaster_to_park():
    '''
    Konnor's Note: I used ChatGPT to generate this JSON File. If you do it that way, make sure to check for any typos
    and that it is formated correctly based on the below example.

    POST 
    {
        "roller_coaster": {
            "name": "Ricochet",                             <-- string
            "park_name": "Carowinds",                       <-- string
            "location": "Charlotte, North Carolina, USA",   <-- string
            "ride_type": "Steel wild mouse coaster",        <-- string
            "height": "54 feet",                            <-- string
            "track_length": "1,195 feet",                   <-- string
            "max_speed": "28 mph",                          <-- string
            "manufacturer": "Mack Rides",                   <-- string
            "year_opened": 2002,                            <-- integer
            "inversions": 0,                                <-- integer
            "tallest_drop": "54 feet",                      <-- string
            "drop_angle": "52 degrees",                     <-- string
        }
    }
    '''
    coaster = request.json["roller_coaster"]

    park = Park.query.filter_by(name=coaster["park_name"], location=coaster["location"]).first()
    if not park:
        return jsonify("The park listed is not in our database. We can't add this coaster to our database."), 400
    
    db.session.merge(Coaster(
        name=coaster["name"],
        year_opened=coaster["year_opened"],
        park_id=park.id,
        ride_type=coaster["ride_type"],
        manufacturer=coaster["manufacturer"],
        track_length=coaster["track_length"],
        height=coaster["height"],
        tallest_drop=coaster["tallest_drop"],
        drop_angle=coaster["drop_angle"],
        max_speed=coaster["max_speed"],
        inversions=coaster["inversions"]
    ))

    db.session.commit()

    return '', 204

@api.route('/coasters/<int:id>', methods=['GET'])
def get_coaster(id):
    coaster = Coaster.query.filter_by(id=id).first()

    return jsonify(coaster.serialize()), 200