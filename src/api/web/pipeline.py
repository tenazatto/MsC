import json

from flask import Blueprint, jsonify, request

from api.service.pipeline import PipelineService

pipeline = Blueprint('pipeline', __name__, url_prefix='/pipeline')
pipeline_service = PipelineService()

@pipeline.route('/manual/single', methods=['POST'])
def manual_pipeline():
    response = jsonify(pipeline_service.single_execution(json.loads(request.data)))
    response.status = 201

    return response

@pipeline.route('/auto', methods=['POST'])
def auto_pipeline():
    response = jsonify(pipeline_service.auto_execution(json.loads(request.data)))
    response.status = 201

    return response