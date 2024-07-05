from db_model.mysql import db, ConvenienceStoreInfo, ConvenienceStoreMap

class DetectService:

    # 지점 조회 예시
    @staticmethod
    def get_all_store_info():
        store_infos = ConvenienceStoreInfo.query.all()
        return [store_info.to_dict() for store_info in store_infos]

    # 지점 생성 예시 
    @staticmethod
    def create_store_info(data):
        new_store_info = ConvenienceStoreInfo(
            storename=data['storename'],
            storerow=data['storerow'],
            storecol=data['storecol']
        )
        db.session.add(new_store_info)
        db.session.commit()
        return new_store_info.to_dict()

    @staticmethod
    def delete_store_info(store_info_id):
        store_info = ConvenienceStoreInfo.query.get(store_info_id)
        if store_info:
            db.session.delete(store_info)
            db.session.commit()
            return True
        return False

    # 편의점 지도
    @staticmethod
    def get_all_store_maps():
        store_maps = ConvenienceStoreMap.query.all()
        return [store_map.to_dict() for store_map in store_maps]

    @staticmethod
    def create_store_map(data):
        # storename으로 편의점 조회
        store_info = db.session.query(ConvenienceStoreInfo).filter_by(storename=data['storename']).first()
        
        if not store_info:
            raise ValueError("Store name not found in ConvenienceStoreInfo")

        # 외래키로 설정
        new_store_map = ConvenienceStoreMap(
            storeinfoid=store_info.id,
            storex=data['storex'],
            storey=data['storey'],
            storestate=data['storestate']
        )
        db.session.add(new_store_map)
        db.session.commit()
        return new_store_map.to_dict()

    @staticmethod
    def delete_store_map(store_map_id):
        store_map = ConvenienceStoreMap.query.get(store_map_id)
        if store_map:
            db.session.delete(store_map)
            db.session.commit()
            return True
        return False