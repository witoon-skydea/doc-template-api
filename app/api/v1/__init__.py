from flask import Blueprint

bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Import routes to register with blueprint
from app.api.v1.routes import templates, documents, stations, flows, auth
