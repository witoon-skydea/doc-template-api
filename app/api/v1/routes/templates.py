from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app import api
from app import db
from app.api.v1.models.models import Template, User
from app.api.v1.schemas.schemas import TemplateSchema
from marshmallow import ValidationError

templates_ns = Namespace('templates', description='Template operations')

# Define models for Swagger documentation
template_model = templates_ns.model('Template', {
    'name': fields.String(required=True, description='Template name'),
    'description': fields.String(description='Template description'),
    'content': fields.String(required=True, description='Template content'),
    'editable_fields': fields.Raw(description='Editable fields in JSON format'),
    'status': fields.String(description='Template status', enum=['draft', 'active', 'archived'])
})

template_response = templates_ns.model('TemplateResponse', {
    'id': fields.Integer(description='Template ID'),
    'public_id': fields.String(description='Public ID'),
    'name': fields.String(description='Template name'),
    'description': fields.String(description='Template description'),
    'content': fields.String(description='Template content'),
    'editable_fields': fields.Raw(description='Editable fields'),
    'status': fields.String(description='Template status'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

template_schema = TemplateSchema()
templates_schema = TemplateSchema(many=True)

# Register namespace with API
api.add_namespace(templates_ns, path='/api/v1/templates')

@templates_ns.route('/')
class TemplateList(Resource):
    @templates_ns.doc('list_templates',
                     params={'status': 'Filter templates by status (draft, active, archived)'},
                     security='Bearer')
    @templates_ns.marshal_list_with(template_response)
    @jwt_required()
    def get(self):
        """Get all templates"""
        # Check for status filter
        status = request.args.get('status')
        
        if status:
            templates = Template.query.filter_by(status=status).order_by(Template.updated_at.desc()).all()
        else:
            templates = Template.query.order_by(Template.updated_at.desc()).all()
        
        return templates_schema.dump(templates)
    
    @templates_ns.doc('create_template', security='Bearer')
    @templates_ns.expect(template_model)
    @templates_ns.response(201, 'Template created', template_response)
    @templates_ns.response(400, 'Validation error')
    @jwt_required()
    def post(self):
        """Create a new template"""
        try:
            # Validate request data
            data = template_schema.load(request.json)
        except ValidationError as err:
            return {"error": "Validation error", "messages": err.messages}, 400
        
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
        
        return template_schema.dump(template), 201


@templates_ns.route('/<string:public_id>')
@templates_ns.param('public_id', 'The template public ID')
class TemplateResource(Resource):
    @templates_ns.doc('get_template', security='Bearer')
    @templates_ns.response(200, 'Success', template_response)
    @templates_ns.response(404, 'Template not found')
    @jwt_required()
    def get(self, public_id):
        """Get a specific template"""
        template = Template.query.filter_by(public_id=public_id).first()
        
        if not template:
            return {"error": "Template not found"}, 404
        
        return template_schema.dump(template)
    
    @templates_ns.doc('update_template', security='Bearer')
    @templates_ns.expect(template_model)
    @templates_ns.response(200, 'Template updated', template_response)
    @templates_ns.response(400, 'Validation error')
    @templates_ns.response(404, 'Template not found')
    @jwt_required()
    def put(self, public_id):
        """Update an existing template"""
        template = Template.query.filter_by(public_id=public_id).first()
        
        if not template:
            return {"error": "Template not found"}, 404
        
        try:
            # Validate request data (partial=True to allow partial updates)
            data = template_schema.load(request.json, partial=True)
        except ValidationError as err:
            return {"error": "Validation error", "messages": err.messages}, 400
        
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
        
        return template_schema.dump(template)
    
    @templates_ns.doc('delete_template', security='Bearer')
    @templates_ns.response(200, 'Template deleted')
    @templates_ns.response(404, 'Template not found')
    @jwt_required()
    def delete(self, public_id):
        """Delete a template"""
        template = Template.query.filter_by(public_id=public_id).first()
        
        if not template:
            return {"error": "Template not found"}, 404
        
        # Delete template
        template.delete()
        
        return {"message": "Template deleted successfully"}
