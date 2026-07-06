import os
from fixit import create_app
from database import db
from dotenv import load_dotenv

load_dotenv()

config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)