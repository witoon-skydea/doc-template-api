from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1 import bp
from app import db
from app.api.v1.models.models import Flow, FlowStep, Station, User
from app.api.v1.schemas.schemas import FlowSchema, FlowStepSchema
from marshmallow import ValidationError
from flasgger import swag_from

flow_schema = FlowSchema()
flows_schema = FlowSchema(many=True)
flow_step_schema = FlowStepSchema()
flow_steps_schema = FlowStepSchema(many=True)

@bp.route('/flows', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Flows'],
    'summary': 'Get all flows',
    'description': 'Returns all document flows',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'active',
            'in': 'query',
            'type': 'boolean',
            'description': 'Filter flows by active status'
        }
    ],
    'responses': {
        '200': {
            'description': 'List of flows',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object'
                }
            }
        }
    }
})
def get_flows():
    """Get all flows"""
    # Check for active filter
    active = request.args.get('active')
    
    if active is not None:
        is_active = active.lower() in ('true', '1', 't', 'y', 'yes')
        flows = Flow.query.filter_by(is_active=is_active).order_by(Flow.name).all()
    else:
        flows = Flow.query.order_by(Flow.name).all()
    
    return jsonify(flows_schema.dump(flows)), 200


@bp.route('/flows/<string:public_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Flows'],
    'summary': 'Get a flow',
    'description': 'Returns a specific document flow',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the flow'
        }
    ],
    'responses': {
        '200': {
            'description': 'Flow details',
            'schema': {
                'type': 'object'
            }
        },
        '404': {
            'description': 'Flow not found'
        }
    }
})
def get_flow(public_id):
    """Get a specific flow"""
    flow = Flow.query.filter_by(public_id=public_id).first()
    
    if not flow:
        return jsonify({"error": "Flow not found"}), 404
    
    return jsonify(flow_schema.dump(flow)), 200


@bp.route('/flows', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Flows'],
    'summary': 'Create a flow',
    'description': 'Create a new document flow',
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
                        'example': 'Approval Flow'
                    },
                    'description': {
                        'type': 'string',
                        'example': 'Standard approval flow for documents'
                    },
                    'is_active': {
                        'type': 'boolean',
                        'example': True
                    }
                },
                'required': ['name']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Flow created',
            'schema': {
                'type': 'object'
            }
        },
        '400': {
            'description': 'Validation error'
        }
    }
})
def create_flow():
    """Create a new flow"""
    try:
        # Validate request data
        data = flow_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Get current user
    identity = get_jwt_identity()
    user = User.query.filter_by(public_id=identity['sub']).first()
    
    # Create flow
    flow = Flow(
        name=data['name'],
        description=data.get('description'),
        is_active=data.get('is_active', True),
        created_by=user.id if user else None
    )
    
    # Save flow to database
    flow.save()
    
    return jsonify(flow_schema.dump(flow)), 201


@bp.route('/flows/<string:public_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Flows'],
    'summary': 'Update a flow',
    'description': 'Update an existing document flow',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the flow'
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
                    'is_active': {
                        'type': 'boolean'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Flow updated',
            'schema': {
                'type': 'object'
            }
        },
        '400': {
            'description': 'Validation error'
        },
        '404': {
            'description': 'Flow not found'
        }
    }
})
def update_flow(public_id):
    """Update an existing flow"""
    flow = Flow.query.filter_by(public_id=public_id).first()
    
    if not flow:
        return jsonify({"error": "Flow not found"}), 404
    
    try:
        # Validate request data (partial=True to allow partial updates)
        data = flow_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Update flow fields
    if 'name' in data:
        flow.name = data['name']
    
    if 'description' in data:
        flow.description = data['description']
    
    if 'is_active' in data:
        flow.is_active = data['is_active']
    
    # Save changes to database
    db.session.commit()
    
    return jsonify(flow_schema.dump(flow)), 200


@bp.route('/flows/<string:public_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Flows'],
    'summary': 'Delete a flow',
    'description': 'Delete an existing document flow',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the flow'
        }
    ],
    'responses': {
        '200': {
            'description': 'Flow deleted',
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
            'description': 'Flow not found'
        }
    }
})
def delete_flow(public_id):
    """Delete a flow"""
    flow = Flow.query.filter_by(public_id=public_id).first()
    
    if not flow:
        return jsonify({"error": "Flow not found"}), 404
    
    # Delete flow steps first (due to foreign key constraint)
    FlowStep.query.filter_by(flow_id=flow.id).delete()
    
    # Delete flow
    flow.delete()
    
    return jsonify({"message": "Flow deleted successfully"}), 200


@bp.route('/flows/<string:public_id>/steps', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Flows'],
    'summary': 'Get flow steps',
    'description': 'Get all steps in a document flow',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the flow'
        }
    ],
    'responses': {
        '200': {
            'description': 'List of flow steps',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object'
                }
            }
        },
        '404': {
            'description': 'Flow not found'
        }
    }
})
def get_flow_steps(public_id):
    """Get all steps in a flow"""
    flow = Flow.query.filter_by(public_id=public_id).first()
    
    if not flow:
        return jsonify({"error": "Flow not found"}), 404
    
    # Get flow steps ordered by order
    steps = FlowStep.query.filter_by(flow_id=flow.id).order_by(FlowStep.order).all()
    
    return jsonify(flow_steps_schema.dump(steps)), 200


@bp.route('/flows/<string:public_id>/steps', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Flows'],
    'summary': 'Add a flow step',
    'description': 'Add a new step to a document flow',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the flow'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'from_station_id': {
                        'type': 'integer',
                        'example': 1
                    },
                    'to_station_id': {
                        'type': 'integer',
                        'example': 2
                    },
                    'condition': {
                        'type': 'string',
                        'example': 'status == "approved"'
                    },
                    'order': {
                        'type': 'integer',
                        'example': 1
                    }
                },
                'required': ['from_station_id', 'to_station_id']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Flow step added',
            'schema': {
                'type': 'object'
            }
        },
        '400': {
            'description': 'Validation error'
        },
        '404': {
            'description': 'Flow or station not found'
        }
    }
})
def add_flow_step(public_id):
    """Add a new step to a flow"""
    flow = Flow.query.filter_by(public_id=public_id).first()
    
    if not flow:
        return jsonify({"error": "Flow not found"}), 404
    
    try:
        # Validate request data
        data = flow_step_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Check if stations exist
    from_station = Station.query.get(data['from_station_id'])
    if not from_station:
        return jsonify({"error": "From station not found"}), 404
    
    to_station = Station.query.get(data['to_station_id'])
    if not to_station:
        return jsonify({"error": "To station not found"}), 404
    
    # Create flow step
    flow_step = FlowStep(
        flow_id=flow.id,
        from_station_id=data['from_station_id'],
        to_station_id=data['to_station_id'],
        condition=data.get('condition'),
        order=data.get('order', 0)
    )
    
    # Save flow step to database
    flow_step.save()
    
    return jsonify(flow_step_schema.dump(flow_step)), 201


@bp.route('/flows/<string:flow_public_id>/steps/<string:step_public_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Flows'],
    'summary': 'Update a flow step',
    'description': 'Update an existing step in a document flow',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'flow_public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the flow'
        },
        {
            'name': 'step_public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the flow step'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'from_station_id': {
                        'type': 'integer'
                    },
                    'to_station_id': {
                        'type': 'integer'
                    },
                    'condition': {
                        'type': 'string'
                    },
                    'order': {
                        'type': 'integer'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Flow step updated',
            'schema': {
                'type': 'object'
            }
        },
        '400': {
            'description': 'Validation error'
        },
        '404': {
            'description': 'Flow, flow step, or station not found'
        }
    }
})
def update_flow_step(flow_public_id, step_public_id):
    """Update an existing flow step"""
    flow = Flow.query.filter_by(public_id=flow_public_id).first()
    
    if not flow:
        return jsonify({"error": "Flow not found"}), 404
    
    flow_step = FlowStep.query.filter_by(public_id=step_public_id, flow_id=flow.id).first()
    
    if not flow_step:
        return jsonify({"error": "Flow step not found"}), 404
    
    try:
        # Validate request data (partial=True to allow partial updates)
        data = flow_step_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Check if stations exist if updating station IDs
    if 'from_station_id' in data:
        from_station = Station.query.get(data['from_station_id'])
        if not from_station:
            return jsonify({"error": "From station not found"}), 404
        flow_step.from_station_id = data['from_station_id']
    
    if 'to_station_id' in data:
        to_station = Station.query.get(data['to_station_id'])
        if not to_station:
            return jsonify({"error": "To station not found"}), 404
        flow_step.to_station_id = data['to_station_id']
    
    # Update other flow step fields
    if 'condition' in data:
        flow_step.condition = data['condition']
    
    if 'order' in data:
        flow_step.order = data['order']
    
    # Save changes to database
    db.session.commit()
    
    return jsonify(flow_step_schema.dump(flow_step)), 200


@bp.route('/flows/<string:flow_public_id>/steps/<string:step_public_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Flows'],
    'summary': 'Delete a flow step',
    'description': 'Delete an existing step from a document flow',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'flow_public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the flow'
        },
        {
            'name': 'step_public_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Public ID of the flow step'
        }
    ],
    'responses': {
        '200': {
            'description': 'Flow step deleted',
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
            'description': 'Flow or flow step not found'
        }
    }
})
def delete_flow_step(flow_public_id, step_public_id):
    """Delete a flow step"""
    flow = Flow.query.filter_by(public_id=flow_public_id).first()
    
    if not flow:
        return jsonify({"error": "Flow not found"}), 404
    
    flow_step = FlowStep.query.filter_by(public_id=step_public_id, flow_id=flow.id).first()
    
    if not flow_step:
        return jsonify({"error": "Flow step not found"}), 404
    
    # Delete flow step
    flow_step.delete()
    
    return jsonify({"message": "Flow step deleted successfully"}), 200
