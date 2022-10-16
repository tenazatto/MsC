import json

from flask import Blueprint, jsonify, request

from src.api.service.config import ConfigService

config = Blueprint('config', __name__, url_prefix='/config')
config_service = ConfigService()

@config.route('/metrics', methods=['GET', 'PUT'])
def metrics_configuration():
    if request.method == 'PUT':
        config_service.save_metrics_configuration(json.loads(request.data))
        response = jsonify(status='Configurações de métricas salvas com sucesso')
        response.status = 201
    else:
        metrics_configuration = config_service.get_metrics_configuration()
        response = jsonify(metrics_configuration)
        response.status = 200

    return response

@config.route('/score', methods=['GET', 'PUT'])
def score_configuration():
    if request.method == 'PUT':
        config_service.save_score_configuration(json.loads(request.data))
        response = jsonify(status='Configurações de pontuação salvas com sucesso')
        response.status = 201
    else:
        score_configuration = config_service.get_score_configuration()
        response = jsonify(score_configuration)
        response.status = 200

    return response

@config.route('/planner', methods=['GET', 'PUT'])
def planner_configuration():
    if request.method == 'PUT':
        config_service.save_planner_configuration(json.loads(request.data))
        response = jsonify(status='Configurações de planejamento salvas com sucesso')
        response.status = 201
    else:
        planner_configuration = config_service.get_planner_configuration()
        response = jsonify(planner_configuration)
        response.status = 200

    return response

@config.route('/analyzer', methods=['GET', 'PUT'])
def analyzer_configuration():
    if request.method == 'PUT':
        config_service.save_analyzer_configuration(json.loads(request.data))
        response = jsonify(status='Configurações de análise salvas com sucesso')
        response.status = 201
    else:
        analyzer_configuration = config_service.get_analyzer_configuration()
        response = jsonify(analyzer_configuration)
        response.status = 200

    return response

@config.route('/valid_algorithms', methods=['GET', 'PUT'])
def valid_algorithms_configuration():
    if request.method == 'PUT':
        config_service.save_valid_algorithms_configuration(json.loads(request.data))
        response = jsonify(status='Configurações de algoritmos válidos salvas com sucesso')
        response.status = 201
    else:
        valid_algorithms_configuration = config_service.get_valid_algorithms_configuration()
        response = jsonify(valid_algorithms_configuration)
        response.status = 200

    return response