from flask import Blueprint, request, jsonify
from detect_products.service.detect_service import DetectService

detect_bp = Blueprint('detect_bp', __name__)

# 엔드포인트 요청

# http://localhost/detect-products/store_infos - 엔드포인트 예시
@detect_bp.route('/store_infos', methods=['GET'])
def get_store_infos():
    store_infos = DetectService.get_all_store_info()
    return jsonify(store_infos)

@detect_bp.route('/store_info', methods=['POST'])
def add_store_info():
    data = request.get_json()
    new_store_info = DetectService.create_store_info(data)
    return jsonify(new_store_info), 201

@detect_bp.route('/store_info/<int:id>', methods=['DELETE'])
def delete_store_info(id):
    result = DetectService.delete_store_info(id)
    if result:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'error': 'Store info not found'}), 404

@detect_bp.route('/store_maps', methods=['GET'])
def get_store_maps():
    store_maps = DetectService.get_all_store_maps()
    return jsonify(store_maps)

@detect_bp.route('/store_map', methods=['POST'])
def add_store_map():
    data = request.json
    try:
        result = DetectService.create_store_map(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@detect_bp.route('/store_map/<int:id>', methods=['DELETE'])
def delete_store_map(id):
    result = DetectService.delete_store_map(id)
    if result:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'error': 'Store map not found'}), 404