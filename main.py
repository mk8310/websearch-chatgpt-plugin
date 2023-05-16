from flask import request, jsonify, send_from_directory
import requests
import os
import json

from context_information import ContextInformation
from utils import process_results

context_information = ContextInformation()

app = context_information.app
logger = context_information.logger


@app.route('/.well-known/ai-plugin.json', methods=['GET'])
def get_plugin_info():
    with open('.well-known/ai-plugin.json') as f:
        data = json.load(f)
        data['api']['url'] = f"{request.scheme}://{request.host}/.well-known/openapi.yaml"
        data['logo_url'] = f"{request.scheme}://{request.host}/.well-known/icon.png"

        return jsonify(data)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    url = f"https://www.googleapis.com/customsearch/v1?key={context_information.api_key}&cx={context_information.cx}&q={query}&num=10"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        results = data.get('items', [])
        formatted_results = process_results(results)
        return jsonify({"results": formatted_results})
    else:
        error_data = response.json()  # Get JSON data from the error response
        logger.error(f"Error fetching search results: {error_data}")  # Print the error data
        return jsonify({"error": "Error fetching search results", "details": error_data}), response.status_code


@app.route('/.well-known/<path:filename>')
def serve_well_known_files(filename):
    return send_from_directory(os.path.join(os.getcwd(), ".well-known"), filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
