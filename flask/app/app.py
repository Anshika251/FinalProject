from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import sys

# Print startup message for debugging
print("Starting Flask application...", file=sys.stderr)

# Initialize Flask app
app = Flask(__name__)

# Database configuration - use SQLite as fallback
database_url = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


try:
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    print(f"Database connection attempted with: {database_url}", file=sys.stderr)
except Exception as e:
    print(f"Database connection error: {e}", file=sys.stderr)
    print("Continuing without database functionality", file=sys.stderr)
    db = None
    migrate = None

# Default route
@app.route('/')
def home():
    db_status = "connected" if db else "not configured"
    return jsonify({
        "message": "Welcome to Flask API with SQLAlchemy",
        "database_status": db_status
    })

# Run the app
if __name__ == '__main__':
    print("Flask app is starting...", file=sys.stderr)
    app.run(host='0.0.0.0', debug=True)