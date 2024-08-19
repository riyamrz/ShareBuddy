#initializes the flask app

from flask import Flask

app = Flask(__name__)  # Creates an instance of the Flask class
app.config.from_object('config')  # Loads configuration settings

from app import routes  # Imports routes from the `routes.py` file
