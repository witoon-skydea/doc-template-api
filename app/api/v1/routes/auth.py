from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.api.v1 import bp
from app import db
from app.api.v1.models.models import User
from app.api.v1.schemas.schemas import UserSchema, LoginSchema
from marshmallow import ValidationError
from datetime import timedelta
from flasgger import swag_from

user_schema = UserSchema()
login_schema = LoginSchema()

@bp.route('/auth/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Register a new user',
    'description': 'Create a new user account',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'example': 'johndoe'
                    },
                    'email': {
                        'type': 'string',
                        'example': 'john@example.com'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'secure_password'
                    }
                },
                'required': ['username', 'email', 'password']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'User registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    },
                    'user': {
                        'type': 'object'
                    }
                }
            }
        },
        '400': {
            'description': 'Validation error or user already exists'
        }
    }
})
def register():
    """Register a new user"""
    try:
        # Validate request data
        data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        role='user'
    )
    user.set_password(data['password'])
    
    # Save user to database
    user.save()
    
    return jsonify({
        "message": "User registered successfully",
        "user": user_schema.dump(user)
    }), 201


@bp.route('/auth/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'User login',
    'description': 'Login to get access token',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'example': 'johndoe'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'secure_password'
                    }
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string'
                    },
                    'user': {
                        'type': 'object'
                    }
                }
            }
        },
        '401': {
            'description': 'Invalid credentials'
        }
    }
})
def login():
    """Login to get access token"""
    try:
        # Validate request data
        data = login_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Check credentials
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    if not user.is_active:
        return jsonify({"error": "Account is inactive"}), 401
    
    # Create access token
    token_data = {
        "sub": user.public_id,
        "username": user.username,
        "role": user.role
    }
    access_token = create_access_token(
        identity=token_data, 
        expires_delta=timedelta(days=1)
    )
    
    return jsonify({
        "access_token": access_token,
        "user": user_schema.dump(user)
    }), 200


@bp.route('/auth/me', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Get current user profile',
    'description': 'Returns current authenticated user information',
    'security': [{'Bearer': []}],
    'responses': {
        '200': {
            'description': 'User profile',
            'schema': {
                'type': 'object'
            }
        },
        '401': {
            'description': 'Not authenticated'
        }
    }
})
def get_user_profile():
    """Get current user profile"""
    identity = get_jwt_identity()
    user = User.query.filter_by(public_id=identity['sub']).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user_schema.dump(user)), 200
