from flask import Blueprint, request, jsonify
from save_map.service.map_service import MapService
from db_model.mysql import db, ConvenienceStoreInfo, ConvenienceStoreMap

map_bp = Blueprint('map_bp', __name__)

# 편의점 지점 조회
@map_bp.route('/store', methods=['GET'])
def get_store():
    store_names = MapService.get_all_store_name()
    return jsonify(store_names)

# 편의점 지도 저장
@map_bp.route('/store/<int:store_id>', methods=['PATCH'])
def update_store(store_id):
    data = request.get_json()
    try:
        updated_map = MapService.update_store(store_id, data)
        return jsonify(updated_map), 200
      
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
@map_bp.route('/<int:store_info_id>', methods=['DELETE'])
def delete_map(store_info_id):
    try:
        MapService.delete_map(store_info_id)
        return jsonify({'message': f'store_info_id: {store_info_id} 삭제 완료'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 404
