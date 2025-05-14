from marshmallow import Schema, fields, validate, validates, ValidationError
import json

class UserSchema(Schema):
    """Schema for User model"""
    id = fields.Int(dump_only=True)
    public_id = fields.Str(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, validate=validate.Length(min=6), required=True)
    role = fields.Str(validate=validate.OneOf(['user', 'admin']), dump_only=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class LoginSchema(Schema):
    """Schema for login credentials"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class TemplateSchema(Schema):
    """Schema for Template model"""
    id = fields.Int(dump_only=True)
    public_id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    description = fields.Str()
    content = fields.Str(required=True)
    editable_fields = fields.Raw()
    status = fields.Str(validate=validate.OneOf(['draft', 'active', 'archived']), default='draft')
    created_by = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('editable_fields')
    def validate_editable_fields(self, value):
        """Validate that editable_fields is valid JSON"""
        if value:
            try:
                if isinstance(value, str):
                    json.loads(value)
            except json.JSONDecodeError:
                raise ValidationError("Editable fields must be valid JSON")


class DocumentSchema(Schema):
    """Schema for Document model"""
    id = fields.Int(dump_only=True)
    public_id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    content = fields.Str(required=True)
    template_id = fields.Int(required=True)
    status = fields.Str(validate=validate.OneOf(['draft', 'submitted', 'approved', 'rejected']), default='draft')
    current_station_id = fields.Int(allow_none=True)
    created_by = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Include related data when needed
    template = fields.Nested('TemplateSchema', exclude=('content', 'editable_fields'), dump_only=True)
    current_station = fields.Nested('StationSchema', exclude=('description',), dump_only=True)


class StationSchema(Schema):
    """Schema for Station model"""
    id = fields.Int(dump_only=True)
    public_id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    description = fields.Str()
    type = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    responsible_role = fields.Str(validate=validate.Length(min=3, max=50))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class FlowSchema(Schema):
    """Schema for Flow model"""
    id = fields.Int(dump_only=True)
    public_id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    description = fields.Str()
    is_active = fields.Bool(default=True)
    created_by = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Include steps when requested
    steps = fields.List(fields.Nested('FlowStepSchema'), dump_only=True)


class FlowStepSchema(Schema):
    """Schema for FlowStep model"""
    id = fields.Int(dump_only=True)
    public_id = fields.Str(dump_only=True)
    flow_id = fields.Int(required=True)
    from_station_id = fields.Int(required=True)
    to_station_id = fields.Int(required=True)
    condition = fields.Str()
    order = fields.Int(default=0)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Include related stations when needed
    from_station = fields.Nested('StationSchema', exclude=('description',), dump_only=True)
    to_station = fields.Nested('StationSchema', exclude=('description',), dump_only=True)


class DocumentHistorySchema(Schema):
    """Schema for DocumentHistory model"""
    id = fields.Int(dump_only=True)
    public_id = fields.Str(dump_only=True)
    document_id = fields.Int(required=True)
    action = fields.Str(required=True)
    description = fields.Str()
    user_id = fields.Int()
    station_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Include related data when needed
    user = fields.Nested('UserSchema', only=('id', 'username', 'email'), dump_only=True)
    station = fields.Nested('StationSchema', only=('id', 'name', 'type'), dump_only=True)
