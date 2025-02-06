import os
import json
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from functools import lru_cache
from typing import List, Dict


class HymnalAPI:
    def __init__(self, directory: str = None):
        self.directory = directory or os.getcwd()
        self.config = self._load_config()
        self.language_map = {item["key"]: item["title"] for item in self.config}
        self.hymnals = self._load_hymnals()

    def _load_config(self) -> List[Dict]:
        """Load configuration from config.json."""
        config_path = os.path.join(self.directory, "config.json")
        try:
            with open(config_path, "r", encoding="utf-8") as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            raise ValueError(f"Config file not found in {self.directory}")

    def _load_hymnals(self) -> Dict:
        """Load hymnal data from JSON files."""
        hymnals = {}
        for filename in os.listdir(self.directory):
            if filename.endswith(".json") and filename != "config.json":
                language = filename.split(".")[0]
                path = os.path.join(self.directory, filename)
                with open(path, "r", encoding="utf-8") as file:
                    hymnals[language] = json.load(file)
        return hymnals

    @lru_cache(maxsize=128)
    def get_languages(self) -> List[str]:
        """Return available languages."""
        return list(self.language_map.keys())

    def get_hymnal_for_language(self, language: str) -> List[Dict]:
        """Retrieve hymns for a specific language."""
        if language not in self.hymnals:
            raise ValueError(f"Language {language} not found")
        return self.hymnals[language]

    def get_specific_hymn(self, language: str, number: int) -> Dict:
        """Find a specific hymn by language and number."""
        hymnal = self.get_hymnal_for_language(language)
        hymn = next((h for h in hymnal if h["number"] == number), None)
        if not hymn:
            raise ValueError(f"Hymn {number} not found in {language}")
        return hymn


def create_app(hymnal_api: HymnalAPI) -> Flask:
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    @app.route('/languages', methods=['GET'])
    def languages():
        try:
            return jsonify(hymnal_api.get_languages())
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/hymnals/<language>', methods=['GET'])
    def hymnals(language):
        try:
            hymns = hymnal_api.get_hymnal_for_language(language)
            return jsonify(hymns)
        except ValueError as e:
            abort(404, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/hymnals/<language>/<int:number>', methods=['GET'])
    def hymn(language, number):
        try:
            hymn = hymnal_api.get_specific_hymn(language, number)
            return jsonify(hymn)
        except ValueError as e:
            abort(404, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/search', methods=['GET'])
    def search_hymns():
        language = request.args.get('language')
        query = request.args.get('query', '').lower()

        if not language:
            abort(400, description="Language parameter is required")

        try:
            hymnal = hymnal_api.get_hymnal_for_language(language)
            results = [
                hymn for hymn in hymnal
                if query in hymn['title'].lower() or query in hymn['content'].lower()
            ]
            return jsonify(results)
        except ValueError as e:
            abort(404, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


# Application setup
hymnal_api = HymnalAPI()
app = create_app(hymnal_api)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
