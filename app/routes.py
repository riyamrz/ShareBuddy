# Contains the routes (URL mappings)

from app import app  # Import the app instance from __init__.py

@app.route('/')
def home():
    return "Welcome to ShareBuddy!"
