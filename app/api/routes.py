from flask import Blueprint, request, jsonify
from ..helpers import token_required
from ..models import db, Venue, Event

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/api/venue', methods=['POST'])
@token_required
def save_venue(our_user):
    venue_data = request.json.get('venue_data')
    tags = request.json.get('tags', [])
    user_token = our_user.token
    saved_venue = Venue.save_venue(venue_data, tags, user_token)

    if saved_venue:
        return jsonify({'message': 'Venue saved successfully', 'venue': saved_venue}), 201
    else:
        return jsonify({'message': 'Failed to save venue'}), 400
