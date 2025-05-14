from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import bp
from app import db
from app.api.v1.models.models import Template, User
from app.api.v1.schemas.schemas import TemplateSchema
from marshmallow import ValidationError
from flasgger import swag_from

template_schema = TemplateSchema()
templates_schema = TemplateSchema(many=True)

@bp.route('/templates', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Templates'],
    'summary': 'Get all templates',
    'description': 'Returns all document templates',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'enum': ['draft', 'active', 'archived'],
            'description': 'Filter templates by status'
        }
    ],
    'responses': {
        '200': {
            'description': 'List of templates',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object'
                }
            }
        }
    }
})
def get_templates():
    """Get all templates"""
    # Check for status filter
    status = request.args.get('status')
    
    if status:
        templates = Template.query.filter_by(status=status).order_by(Template.updated_at.desc()).all()
    else:
        templates = Template.query.order_by(Template.updated_at.desc()).all()
    
    return jsonify(templates_schema.dump(templates)), 200


@bp.route('/templates/<string:public_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Templates'],
    'summary': 'Get a template',
    'description': 'Returns a specific document template',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the template'
        }
    ],
    'responses': {
        '200': {
            'description': 'Template details',
            'schema': {
                'type': 'object'
            }
        },
        '404': {
            'description': 'Template not found'
        }
    }
})
def get_template(public_id):
    """Get a specific template"""
    template = Template.query.filter_by(public_id=public_id).first()
    
    if not template:
        return jsonify({"error": "Template not found"}), 404
    
    return jsonify(template_schema.dump(template)), 200


@bp.route('/templates', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Templates'],
    'summary': 'Create a template',
    'description': 'Create a new document template',
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
                        'example': 'Invoice Template'
                    },
                    'description': {
                        'type': 'string',
                        'example': 'Template for creating invoices'
                    },
                    'content': {
                        'type': 'string',
                        'example': '<html><body>Invoice content...</body></html>'
                    },
                    'editable_fields': {
                        'type': 'object',
                        'example': {
                            'fields': [
                                {'name': 'customer_name', 'type': 'text'},
                                {'name': 'amount', 'type': 'number'}
                            ]
                        }
                    },
                    'status': {
                        'type': 'string',
                        'enum': ['draft', 'active', 'archived'],
                        'example': 'draft'
                    }
                },
                'required': ['name', 'content']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Template created',
            'schema': {
                'type': 'object'
            }
        },
        '400': {
            'description': 'Validation error'
        }
    }
})
def create_template():
    """Create a new template"""
    try:
        # Validate request data
        data = template_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Get current user
    identity = get_jwt_identity()
    user = User.query.filter_by(public_id=identity['sub']).first()
    
    # Create template
    template = Template(
        name=data['name'],
        description=data.get('description'),
        content=data['content'],
        status=data.get('status', 'draft'),
        created_by=user.id if user else None
    )
    
    # Set editable fields if provided
    editable_fields = data.get('editable_fields')
    if editable_fields:
        template.set_editable_fields(editable_fields)
    
    # Save template to database
    template.save()
    
    return jsonify(template_schema.dump(template)), 201


@bp.route('/templates/<string:public_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Templates'],
    'summary': 'Update a template',
    'description': 'Update an existing document template',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the template'
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
                    'content': {
                        'type': 'string'
                    },
                    'editable_fields': {
                        'type': 'object'
                    },
                    'status': {
                        'type': 'string',
                        'enum': ['draft', 'active', 'archived']
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Template updated',
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
def update_template(public_id):
    """Update an existing template"""
    template = Template.query.filter_by(public_id=public_id).first()
    
    if not template:
        return jsonify({"error": "Template not found"}), 404
    
    try:
        # Validate request data (partial=True to allow partial updates)
        data = template_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Update template fields
    if 'name' in data:
        template.name = data['name']
    
    if 'description' in data:
        template.description = data['description']
    
    if 'content' in data:
        template.content = data['content']
    
    if 'status' in data:
        template.status = data['status']
    
    if 'editable_fields' in data:
        template.set_editable_fields(data['editable_fields'])
    
    # Save changes to database
    db.session.commit()
    
    return jsonify(template_schema.dump(template)), 200


@bp.route('/templates/<string:public_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Templates'],
    'summary': 'Delete a template',
    'description': 'Delete an existing document template',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the template'
        }
    ],
    'responses': {
        '200': {
            'description': 'Template deleted',
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
            'description': 'Template not found'
        }
    }
})
def delete_template(public_id):
    """Delete a template"""
    template = Template.query.filter_by(public_id=public_id).first()
    
    if not template:
        return jsonify({"error": "Template not found"}), 404
    
    # Delete template
    template.delete()
    
    return jsonify({"message": "Template deleted successfully"}), 200
