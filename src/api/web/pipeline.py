import json

from flask import Blueprint, jsonify, request

from src.api.service.pipeline import PipelineService

pipeline = Blueprint('pipeline', __name__, url_prefix='/pipeline')
pipeline_service = PipelineService()


@pipeline.route('/manual/single', methods=['POST'])
@pipeline.route('/auto/single', methods=['POST'])
def manual_pipeline():
    response = jsonify(pipeline_service.single_execution(json.loads(request.data)))
    response.status = 201

    return response


@pipeline.route('/auto/plans', methods=['GET'])
def auto_pipeline():
    num_pipelines = request.args.get('num_pipelines', default=1, type=int)
    dataset = request.args.get('dataset')
    preprocessor = request.args.get('preprocessor', default='')

    response = jsonify(pipeline_service.auto_execution(num_pipelines, dataset, preprocessor))
    response.status = 200

    return response