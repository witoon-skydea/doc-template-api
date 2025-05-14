from flask import Blueprint

bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Import routes to initialize REST namespaces
from app.api.v1.routes import templates
# The following will be updated later
# from app.api.v1.routes import documents, stations, flows, auth
