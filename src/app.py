import os
import cloudinary
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from models import db

from routes import auth

load_dotenv()

app = Flask(__name__)

app.config['DEBUG'] = True # Permite ver los errores
app.config['ENV'] = 'development' # Activa el servidor en modo desarrollo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASEURI') # Leemos la url de conexion a la base de datos
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_CLOUD_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_CLOUD_API_SECRET'),
    secure=True
)

app.register_blueprint(auth.bpAuth, url_prefix="/api") # /api/login, /api/register

if __name__ == '__main__':
    app.run()
