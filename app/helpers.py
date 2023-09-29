
from flask import request, jsonify, json, current_app
from functools import wraps
from .models import User
import secrets, decimal, inspect, requests, os

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

def token_required(flask_function):
    @wraps(flask_function)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
        elif 'token' in request.form:
            token = request.form['token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            our_user = User.query.filter_by(token=token).first()
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'}), 401
        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        if 'our_user' in inspect.signature(flask_function).parameters:
            return flask_function(our_user, *args, **kwargs)
        else:
            return flask_function(*args, **kwargs)
    return decorated

# def search_venues(query: str) -> dict:
#     url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={os.getenv('GOOGLE_MAPS_KEY')}"
#     response = requests.get(url)
#     data = response.json()
#     return data

# def get_venue_details(venue_id: str) -> dict:
#     url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={venue_id}&key={os.getenv('GOOGLE_MAPS_KEY')}"
#     response = requests.get(url)
#     data = response.json()
#     return data