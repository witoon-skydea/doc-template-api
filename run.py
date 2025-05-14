import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create application instance
app = create_app()

if __name__ == '__main__':
    # Get port from environment or use default (8531)
    port = int(os.environ.get('API_PORT', 8531))
    debug = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    
    # Run application
    app.run(host='0.0.0.0', port=port, debug=debug)
