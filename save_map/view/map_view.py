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
@map_bp.route('/store', methods=['POST'])
def save_store():
    data = request.get_json()

    # 필수 필드 확인
    required_fields = ['storename', 'storerow', 'storecol', 'maps']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
    # StoreService를 사용하여 데이터 저장
        store_data = MapService.save_store(data)
        return jsonify({"message": "점주 지도 등록이 완료되었습니다."}), 201

    except ValueError:
    # ValueError 발생 시 실패 메시지
        return jsonify({"message": "점주 지도 등록에 실패하였습니다."}), 400

    except Exception:
    # 기타 예외 발생 시 실패 메시지
        return jsonify({"message": "점주 지도 등록에 실패하였습니다."}), 500
    
# 편의점 지도 수정
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
