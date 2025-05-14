from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import bp
from app import db
from app.api.v1.models.models import Station, Document
from app.api.v1.schemas.schemas import StationSchema
from marshmallow import ValidationError
from flasgger import swag_from

station_schema = StationSchema()
stations_schema = StationSchema(many=True)

@bp.route('/stations', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Stations'],
    'summary': 'Get all stations',
    'description': 'Returns all stations',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'type',
            'in': 'query',
            'type': 'string',
            'description': 'Filter stations by type'
        }
    ],
    'responses': {
        '200': {
            'description': 'List of stations',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object'
                }
            }
        }
    }
})
def get_stations():
    """Get all stations"""
    # Check for type filter
    station_type = request.args.get('type')
    
    if station_type:
        stations = Station.query.filter_by(type=station_type).order_by(Station.name).all()
    else:
        stations = Station.query.order_by(Station.name).all()
    
    return jsonify(stations_schema.dump(stations)), 200


@bp.route('/stations/<string:public_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Stations'],
    'summary': 'Get a station',
    'description': 'Returns a specific station',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the station'
        }
    ],
    'responses': {
        '200': {
            'description': 'Station details',
            'schema': {
                'type': 'object'
            }
        },
        '404': {
            'description': 'Station not found'
        }
    }
})
def get_station(public_id):
    """Get a specific station"""
    station = Station.query.filter_by(public_id=public_id).first()
    
    if not station:
        return jsonify({"error": "Station not found"}), 404
    
    return jsonify(station_schema.dump(station)), 200


@bp.route('/stations', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Stations'],
    'summary': 'Create a station',
    'description': 'Create a new station',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'Approval Station'
                    },
                    'description': {
                        'type': 'string',
                        'example': 'Station for document approval'
                    },
                    'type': {
                        'type': 'string',
                        'example': 'approval'
                    },
                    'responsible_role': {
                        'type': 'string',
                        'example': 'admin'
                    }
                },
                'required': ['name', 'type']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Station created',
            'schema': {
                'type': 'object'
            }
        },
        '400': {
            'description': 'Validation error'
        }
    }
})
def create_station():
    """Create a new station"""
    try:
        # Validate request data
        data = station_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Create station
    station = Station(
        name=data['name'],
        description=data.get('description'),
        type=data['type'],
        responsible_role=data.get('responsible_role')
    )
    
    # Save station to database
    station.save()
    
    return jsonify(station_schema.dump(station)), 201


@bp.route('/stations/<string:public_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Stations'],
    'summary': 'Update a station',
    'description': 'Update an existing station',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the station'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string'
                    },
                    'description': {
                        'type': 'string'
                    },
                    'type': {
                        'type': 'string'
                    },
                    'responsible_role': {
                        'type': 'string'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Station updated',
            'schema': {
                'type': 'object'
            }
        },
        '400': {
            'description': 'Validation error'
        },
        '404': {
            'description': 'Station not found'
        }
    }
})
def update_station(public_id):
    """Update an existing station"""
    station = Station.query.filter_by(public_id=public_id).first()
    
    if not station:
        return jsonify({"error": "Station not found"}), 404
    
    try:
        # Validate request data (partial=True to allow partial updates)
        data = station_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Update station fields
    if 'name' in data:
        station.name = data['name']
    
    if 'description' in data:
        station.description = data['description']
    
    if 'type' in data:
        station.type = data['type']
    
    if 'responsible_role' in data:
        station.responsible_role = data['responsible_role']
    
    # Save changes to database
    db.session.commit()
    
    return jsonify(station_schema.dump(station)), 200


@bp.route('/stations/<string:public_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Stations'],
    'summary': 'Delete a station',
    'description': 'Delete an existing station',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the station'
        }
    ],
    'responses': {
        '200': {
            'description': 'Station deleted',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                }
            }
        },
        '400': {
            'description': 'Station has documents and cannot be deleted'
        },
        '404': {
            'description': 'Station not found'
        }
    }
})
def delete_station(public_id):
    """Delete a station"""
    station = Station.query.filter_by(public_id=public_id).first()
    
    if not station:
        return jsonify({"error": "Station not found"}), 404
    
    # Check if any documents are currently at this station
    documents_at_station = Document.query.filter_by(current_station_id=station.id).count()
    if documents_at_station > 0:
        return jsonify({"error": "Cannot delete station with active documents"}), 400
    
    # Delete station
    station.delete()
    
    return jsonify({"message": "Station deleted successfully"}), 200


@bp.route('/stations/<string:public_id>/documents', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Stations'],
    'summary': 'Get documents at a station',
    'description': 'Get all documents currently at a specific station',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the station'
        },
        {
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'enum': ['draft', 'submitted', 'approved', 'rejected'],
            'description': 'Filter documents by status'
        }
    ],
    'responses': {
        '200': {
            'description': 'List of documents at the station',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object'
                }
            }
        },
        '404': {
            'description': 'Station not found'
        }
    }
})
def get_station_documents(public_id):
    """Get all documents at a station"""
    from app.api.v1.schemas.schemas import DocumentSchema
    
    station = Station.query.filter_by(public_id=public_id).first()
    
    if not station:
        return jsonify({"error": "Station not found"}), 404
    
    # Build query for documents at this station
    query = Document.query.filter_by(current_station_id=station.id)
    
    # Apply status filter if provided
    status = request.args.get('status')
    if status:
        query = query.filter_by(status=status)
    
    # Get documents ordered by last update
    documents = query.order_by(Document.updated_at.desc()).all()
    
    # Use DocumentSchema to serialize
    documents_schema = DocumentSchema(many=True)
    
    return jsonify(documents_schema.dump(documents)), 200
