from app import db
from datetime import datetime
import uuid

class Base(db.Model):
    """Base model that other models will inherit from"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Save the model instance to the database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete the model instance from the database"""
        db.session.delete(self)
        db.session.commit()
