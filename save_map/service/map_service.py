from db_model.mysql import db, ConvenienceStoreInfo, ConvenienceStoreMap

class MapService:
  
  @staticmethod
  def get_all_store_name():
    store_names = ConvenienceStoreInfo.query.all()
    return [store_name.to_id() for store_name in store_names]
  
  @staticmethod
  def update_store(store_id, data):
    # 기존 ConvenienceStoreInfo 조회
    store_info = ConvenienceStoreInfo.query.get_or_404(store_id)

    # 편의점 정보 업데이트(patch매핑이라 if문으로 처리)
    if 'storerow' in data:
        store_info.storerow = data['storerow']
    if 'storecol' in data:
        store_info.storecol = data['storecol']

    # 지도 정보 업데이트
    if 'maps' in data:
            for map_data in data['maps']:
                new_map_instance = ConvenienceStoreMap(
                    storex=map_data['storex'],
                    storey=map_data['storey'],
                    storestate=map_data['storestate'],
                    storeinfoid=store_info.id
                )
                db.session.add(new_map_instance)

    db.session.commit()

    return store_info.to_id()

  @staticmethod
  def delete_map(store_info_id):
    map_instances = ConvenienceStoreMap.query.filter_by(storeinfoid=store_info_id).all()
    if not map_instances:
        raise ValueError(f"store_info_id가 {store_info_id} 없습니다.")
    
    for map_instance in map_instances:
        db.session.delete(map_instance)
    
    db.session.commit()
