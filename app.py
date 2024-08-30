from flask import Flask
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)  # Create a Flask app
app.config.from_object(Config)  # Load configuration from Config class
mysql = MySQL(app)  # Initialize MySQL