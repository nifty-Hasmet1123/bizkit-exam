"""
Entry point for running the Flask application.

This script initializes and runs the Flask application defined in the phasebook __init__ file.

Usage:
    python run.py

Note:
    Ensure that the 'app' module is properly configured with routes and settings.
"""

from phasebook import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug = True)