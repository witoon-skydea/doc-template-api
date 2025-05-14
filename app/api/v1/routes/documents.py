from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import bp
from app import db
from app.api.v1.models.models import Document, Template, User, DocumentHistory, Station
from app.api.v1.schemas.schemas import DocumentSchema, DocumentHistorySchema
from marshmallow import ValidationError
from flasgger import swag_from

document_schema = DocumentSchema()
documents_schema = DocumentSchema(many=True)
history_schema = DocumentHistorySchema()
history_list_schema = DocumentHistorySchema(many=True)

@bp.route('/documents', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Documents'],
    'summary': 'Get all documents',
    'description': 'Returns all documents',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'enum': ['draft', 'submitted', 'approved', 'rejected'],
            'description': 'Filter documents by status'
        },
        {
            'name': 'template_id',
            'in': 'query',
            'type': 'string',
            'description': 'Filter documents by template public ID'
        },
        {
            'name': 'station_id',
            'in': 'query',
            'type': 'string',
            'description': 'Filter documents by current station public ID'
        }
    ],
    'responses': {
        '200': {
            'description': 'List of documents',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object'
                }
            }
        }
    }
})
def get_documents():
    """Get all documents"""
    query = Document.query
    
    # Apply filters
    status = request.args.get('status')
    if status:
        query = query.filter_by(status=status)
    
    template_id = request.args.get('template_id')
    if template_id:
        template = Template.query.filter_by(public_id=template_id).first()
        if template:
            query = query.filter_by(template_id=template.id)
    
    station_id = request.args.get('station_id')
    if station_id:
        station = Station.query.filter_by(public_id=station_id).first()
        if station:
            query = query.filter_by(current_station_id=station.id)
    
    # Get results ordered by last update
    documents = query.order_by(Document.updated_at.desc()).all()
    
    return jsonify(documents_schema.dump(documents)), 200


@bp.route('/documents/<string:public_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Documents'],
    'summary': 'Get a document',
    'description': 'Returns a specific document',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the document'
        }
    ],
    'responses': {
        '200': {
            'description': 'Document details',
            'schema': {
                'type': 'object'
            }
        },
        '404': {
            'description': 'Document not found'
        }
    }
})
def get_document(public_id):
    """Get a specific document"""
    document = Document.query.filter_by(public_id=public_id).first()
    
    if not document:
        return jsonify({"error": "Document not found"}), 404
    
    return jsonify(document_schema.dump(document)), 200


@bp.route('/documents', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Documents'],
    'summary': 'Create a document',
    'description': 'Create a new document from a template',
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
                        'example': 'Invoice #12345'
                    },
                    'content': {
                        'type': 'string',
                        'example': '<html><body>Invoice content...</body></html>'
                    },
                    'template_id': {
                        'type': 'integer',
                        'example': 1
                    },
                    'status': {
                        'type': 'string',
                        'enum': ['draft', 'submitted', 'approved', 'rejected'],
                        'example': 'draft'
                    },
                    'current_station_id': {
                        'type': 'integer',
                        'example': 1
                    }
                },
                'required': ['name', 'content', 'template_id']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Document created',
            'schema': {
                'type': 'object'
            }
        },
        '400': {
            'description': 'Validation error'
        },
        '404': {
            'description': 'Template not found'
        }
    }
})
def create_document():
    """Create a new document"""
    try:
        # Validate request data
        data = document_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Check if template exists
    template = Template.query.get(data['template_id'])
    if not template:
        return jsonify({"error": "Template not found"}), 404
    
    # Get current user
    identity = get_jwt_identity()
    user = User.query.filter_by(public_id=identity['sub']).first()
    
    # Create document
    document = Document(
        name=data['name'],
        content=data['content'],
        template_id=data['template_id'],
        status=data.get('status', 'draft'),
        current_station_id=data.get('current_station_id'),
        created_by=user.id if user else None
    )
    
    # Save document to database
    document.save()
    
    # Create document history entry
    history = DocumentHistory(
        document_id=document.id,
        action='created',
        description='Document created',
        user_id=user.id if user else None,
        station_id=document.current_station_id
    )
    
    # Save history to database
    history.save()
    
    return jsonify(document_schema.dump(document)), 201


@bp.route('/documents/<string:public_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Documents'],
    'summary': 'Update a document',
    'description': 'Update an existing document',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the document'
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
                    'content': {
                        'type': 'string'
                    },
                    'status': {
                        'type': 'string',
                        'enum': ['draft', 'submitted', 'approved', 'rejected']
                    },
                    'current_station_id': {
                        'type': 'integer'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Document updated',
            'schema': {
                'type': 'object'
            }
        },
        '400': {
            'description': 'Validation error'
        },
        '404': {
            'description': 'Document not found'
        }
    }
})
def update_document(public_id):
    """Update an existing document"""
    document = Document.query.filter_by(public_id=public_id).first()
    
    if not document:
        return jsonify({"error": "Document not found"}), 404
    
    try:
        # Validate request data (partial=True to allow partial updates)
        data = document_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Get current user
    identity = get_jwt_identity()
    user = User.query.filter_by(public_id=identity['sub']).first()
    
    # Track if station changed
    old_station_id = document.current_station_id
    
    # Update document fields
    if 'name' in data:
        document.name = data['name']
    
    if 'content' in data:
        document.content = data['content']
    
    if 'status' in data:
        document.status = data['status']
    
    if 'current_station_id' in data:
        document.current_station_id = data['current_station_id']
    
    # Save changes to database
    db.session.commit()
    
    # Create document history entry
    description = 'Document updated'
    action = 'updated'
    
    # If station changed, create a 'moved' history entry
    if 'current_station_id' in data and old_station_id != document.current_station_id:
        action = 'moved'
        old_station = Station.query.get(old_station_id) if old_station_id else None
        new_station = Station.query.get(document.current_station_id) if document.current_station_id else None
        
        if old_station and new_station:
            description = f'Moved from {old_station.name} to {new_station.name}'
        elif new_station:
            description = f'Moved to {new_station.name}'
        else:
            description = 'Removed from station'
    
    history = DocumentHistory(
        document_id=document.id,
        action=action,
        description=description,
        user_id=user.id if user else None,
        station_id=document.current_station_id
    )
    
    # Save history to database
    history.save()
    
    return jsonify(document_schema.dump(document)), 200


@bp.route('/documents/<string:public_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Documents'],
    'summary': 'Delete a document',
    'description': 'Delete an existing document',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the document'
        }
    ],
    'responses': {
        '200': {
            'description': 'Document deleted',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                }
            }
        },
        '404': {
            'description': 'Document not found'
        }
    }
})
def delete_document(public_id):
    """Delete a document"""
    document = Document.query.filter_by(public_id=public_id).first()
    
    if not document:
        return jsonify({"error": "Document not found"}), 404
    
    # Delete document history first (due to foreign key constraint)
    DocumentHistory.query.filter_by(document_id=document.id).delete()
    
    # Delete document
    document.delete()
    
    return jsonify({"message": "Document deleted successfully"}), 200


@bp.route('/documents/<string:public_id>/history', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Documents'],
    'summary': 'Get document history',
    'description': 'Get the history of a document',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the document'
        }
    ],
    'responses': {
        '200': {
            'description': 'Document history',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object'
                }
            }
        },
        '404': {
            'description': 'Document not found'
        }
    }
})
def get_document_history(public_id):
    """Get the history of a document"""
    document = Document.query.filter_by(public_id=public_id).first()
    
    if not document:
        return jsonify({"error": "Document not found"}), 404
    
    # Get document history ordered by creation date
    history = DocumentHistory.query.filter_by(document_id=document.id).order_by(DocumentHistory.created_at.desc()).all()
    
    return jsonify(history_list_schema.dump(history)), 200
