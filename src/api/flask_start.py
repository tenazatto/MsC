from flask import Flask
from flask_cors import CORS

from src.api.web.config import config
from src.api.web.pipeline import pipeline

api = Flask(__name__)
api.register_blueprint(config)
api.register_blueprint(pipeline)
CORS(api)

if __name__ == '__main__':
    api.run(port=8080)
