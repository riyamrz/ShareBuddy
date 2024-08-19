# Script to run the Flask app

from app import app

if __name__ == "__main__":
    app.run(debug=True)  # Starts the Flask app in debug mode
