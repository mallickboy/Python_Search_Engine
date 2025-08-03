#!/usr/bin/env python3

from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from search import perform_search

import sys
print("Running with:", sys.executable)


app = Flask(__name__)

CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query or not query.strip():
        return jsonify({"error": "Empty query"}), 400
    try:
        results = perform_search(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
 