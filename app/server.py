from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from search import perform_search

app = Flask(__name__)

CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if query:
        results = perform_search(query)
        return jsonify(results)
        # return jsonify({'query': query, 'results': results})
    return jsonify({"error": "No query parameter provided"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=8080)
 