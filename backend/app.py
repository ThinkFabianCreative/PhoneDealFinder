#!/usr/bin/env python3
"""
Flask API for iPhone Price Monitor
Serves price data and static frontend files.
"""

import os
import json
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='../web_ui/build', static_url_path='')
CORS(app)  # Enable CORS for development

PRICES_FILE = os.path.join(os.path.dirname(__file__), 'prices.json')


@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Return all price data from prices.json."""
    try:
        if os.path.exists(PRICES_FILE):
            with open(PRICES_FILE, 'r') as f:
                prices = json.load(f)
            return jsonify(prices)
        else:
            return jsonify([]), 200
    except (json.JSONDecodeError, IOError) as e:
        return jsonify({'error': f'Error reading prices file: {str(e)}'}), 500


@app.route('/test.html')
def serve_test():
    """Serve simple test page."""
    test_file = os.path.join(os.path.dirname(__file__), '..', 'test.html')
    if os.path.exists(test_file):
        return send_from_directory(os.path.dirname(test_file), 'test.html')
    return "Test file not found", 404

@app.route('/')
def serve_frontend():
    """Serve React frontend index.html."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from React build."""
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    # For React Router, fallback to index.html
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5001)

