# This is a file where you'll store configuration settings for your Flask app.
# Create this file manually in the root directory of your project (ShareBuddy/).

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
