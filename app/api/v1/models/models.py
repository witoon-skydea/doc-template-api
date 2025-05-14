from app import db
from app.api.v1.models.base import Base
from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = 'users'
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash the password for storage"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the password matches the hash"""
        return check_password_hash(self.password_hash, password)


class Template(Base):
    """Document template model"""
    __tablename__ = 'templates'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=False)
    editable_fields = db.Column(db.Text, nullable=True)  # Stored as JSON
    status = db.Column(db.String(20), default='draft')  # draft, active, archived
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    documents = db.relationship('Document', backref='template', lazy=True)
    creator = db.relationship('User', backref='created_templates', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<Template {self.name}>'
    
    def get_editable_fields(self):
        """Get the list of editable fields"""
        if self.editable_fields:
            return json.loads(self.editable_fields)
        return []
    
    def set_editable_fields(self, fields):
        """Set the list of editable fields"""
        self.editable_fields = json.dumps(fields)


class Document(Base):
    """Document model created from templates"""
    __tablename__ = 'documents'
    
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, submitted, approved, rejected
    current_station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    document_history = db.relationship('DocumentHistory', backref='document', lazy=True)
    creator = db.relationship('User', backref='created_documents', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<Document {self.name}>'


class Station(Base):
    """Station model for document workflow"""
    __tablename__ = 'stations'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(50), nullable=False)  # approval, signature, review, etc.
    responsible_role = db.Column(db.String(50), nullable=True)  # Role required to process at this station
    
    # Relationships
    documents = db.relationship('Document', backref='current_station', lazy=True, foreign_keys=[Document.current_station_id])
    flow_steps_from = db.relationship('FlowStep', backref='from_station', lazy=True, foreign_keys='FlowStep.from_station_id')
    flow_steps_to = db.relationship('FlowStep', backref='to_station', lazy=True, foreign_keys='FlowStep.to_station_id')
    
    def __repr__(self):
        return f'<Station {self.name}>'


class Flow(Base):
    """Flow model for document workflow"""
    __tablename__ = 'flows'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    steps = db.relationship('FlowStep', backref='flow', lazy=True)
    creator = db.relationship('User', backref='created_flows', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<Flow {self.name}>'


class FlowStep(Base):
    """Flow step model for document workflow"""
    __tablename__ = 'flow_steps'
    
    flow_id = db.Column(db.Integer, db.ForeignKey('flows.id'), nullable=False)
    from_station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    to_station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    condition = db.Column(db.String(255), nullable=True)  # Condition for transition
    order = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<FlowStep {self.id}>'


class DocumentHistory(Base):
    """Document history model for tracking changes"""
    __tablename__ = 'document_history'
    
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # created, updated, moved, etc.
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='document_history_entries')
    station = db.relationship('Station', backref='document_history_entries')
    
    def __repr__(self):
        return f'<DocumentHistory {self.action} at {self.created_at}>'
