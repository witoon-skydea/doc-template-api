import pytest
import os
import tempfile
from app import create_app, db
from app.api.v1.models.models import User, Template, Station, Flow, FlowStep

@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    # Create the app with test config
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-key',
        'JWT_SECRET_KEY': 'jwt-test-key'
    })
    
    # Create the database and the tables
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app"""
    return app.test_cli_runner()

class AuthActions:
    """Class to help with authentication in tests"""
    def __init__(self, client):
        self._client = client
    
    def register(self, username='test', email='test@example.com', password='test-password'):
        """Register a test user"""
        return self._client.post(
            '/api/v1/auth/register',
            json={'username': username, 'email': email, 'password': password}
        )
    
    def login(self, username='test', password='test-password'):
        """Login as test user"""
        return self._client.post(
            '/api/v1/auth/login',
            json={'username': username, 'password': password}
        )
    
    def get_token(self, username='test', password='test-password'):
        """Get token for test user"""
        response = self.login(username, password)
        return response.get_json()['access_token']

@pytest.fixture
def auth(client):
    """Authentication fixture"""
    return AuthActions(client)

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'

def test_register(client):
    """Test user registration"""
    response = client.post(
        '/api/v1/auth/register',
        json={'username': 'test', 'email': 'test@example.com', 'password': 'test-password'}
    )
    assert response.status_code == 201
    assert 'user' in response.get_json()
    assert response.get_json()['user']['username'] == 'test'

def test_login(client, auth):
    """Test user login"""
    # Register first
    auth.register()
    
    # Then login
    response = auth.login()
    assert response.status_code == 200
    assert 'access_token' in response.get_json()
    assert 'user' in response.get_json()

def test_get_user_profile(client, auth):
    """Test getting user profile"""
    # Register and login
    auth.register()
    token = auth.get_token()
    
    # Get profile
    response = client.get(
        '/api/v1/auth/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.get_json()['username'] == 'test'

def test_create_template(client, auth, app):
    """Test creating a template"""
    # Register and login
    auth.register()
    token = auth.get_token()
    
    # Create template
    response = client.post(
        '/api/v1/templates',
        json={
            'name': 'Test Template',
            'description': 'Template for testing',
            'content': '<html><body>Test content</body></html>',
            'editable_fields': {
                'fields': [
                    {'name': 'test_field', 'type': 'text'}
                ]
            },
            'status': 'draft'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    assert response.get_json()['name'] == 'Test Template'
    
    # Check database
    with app.app_context():
        template = Template.query.filter_by(name='Test Template').first()
        assert template is not None
        assert template.status == 'draft'

def test_create_station(client, auth, app):
    """Test creating a station"""
    # Register and login
    auth.register()
    token = auth.get_token()
    
    # Create station
    response = client.post(
        '/api/v1/stations',
        json={
            'name': 'Test Station',
            'description': 'Station for testing',
            'type': 'test',
            'responsible_role': 'user'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    assert response.get_json()['name'] == 'Test Station'
    
    # Check database
    with app.app_context():
        station = Station.query.filter_by(name='Test Station').first()
        assert station is not None
        assert station.type == 'test'

def test_create_flow(client, auth, app):
    """Test creating a flow"""
    # Register and login
    auth.register()
    token = auth.get_token()
    
    # Create flow
    response = client.post(
        '/api/v1/flows',
        json={
            'name': 'Test Flow',
            'description': 'Flow for testing',
            'is_active': True
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    assert response.get_json()['name'] == 'Test Flow'
    
    # Check database
    with app.app_context():
        flow = Flow.query.filter_by(name='Test Flow').first()
        assert flow is not None
        assert flow.is_active == True
