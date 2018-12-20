import os
from flask_migrate import Migrate
from app import create_app
from app import db
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = create_app(os.getenv('APP_CONFIG') or 'default')
migrate = Migrate(app, db)