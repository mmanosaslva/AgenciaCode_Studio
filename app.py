import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.database.seed import seed_database

flask_app = create_app()

with flask_app.app_context():
    seed_database()

if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0', port=5000)
