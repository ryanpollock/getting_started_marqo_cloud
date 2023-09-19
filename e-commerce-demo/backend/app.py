import logging
from flask import Flask, jsonify, request
from marqo_search import search
from models import SearchSettings
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/api/health", methods=["GET"])
def health():
    response = {"status": "Backend is healthy."}
    return jsonify(response), 200


@app.route("/api/search_marqo", methods=["POST"])
def search_marqo():
    data = request.get_json()
    app.logger.debug(f"Data recieved: {data}")
    query = data.get("query")
    more_of = data.get("moreOf")
    less_of = data.get("lessOf")
    custom_instructions = data.get("customInstructions")
    limit = data.get("limit")
    favourites = data.get("favourites")
    search_settings = SearchSettings.from_dict(data.get("searchSettings"))

    try:
        results = search(query, more_of, less_of, custom_instructions, favourites, limit, search_settings)
        app.logger.debug(f"Found {len(results)} results")
    except Exception as e:
        app.logger.debug(str(e))

    response = {"results": [dict(r) for r in results]}
    return response, 200


if __name__ == "__main__":
    app.run(debug=True)


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
