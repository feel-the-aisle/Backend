from flask import Flask
from db_model.mysql import db
from flask_migrate import Migrate
import os

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('.env')

    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        db.drop_all()  # 기존 테이블 삭제
        db.create_all()  # 테이블 생성
        insert_dummy_data()
        
        # 각 기능의 엔드포인트 위치
        # url_prefix는 엔드포인트 앞에 붙는 경로임
        from detect_products.view.detect_view import detect_bp
        app.register_blueprint(detect_bp, url_prefix='/detect-products')
        
        from search_recipes.view.search_view import search_bp
        app.register_blueprint(search_bp, url_prefix='/gpt-ramen')
        
        from save_map.view.map_view import map_bp
        app.register_blueprint(map_bp, url_prefix='/map')

        from find_path.view.find_view import findpath_bp
        app.register_blueprint(findpath_bp, url_prefix='/find-path')
        
    return app

def insert_dummy_data():
    from db_model.mysql import ConvenienceStoreInfo, ConvenienceStoreMap
    
    # 더미 데이터 생성
    store1 = ConvenienceStoreInfo(storename="미래혁신관 CU")
    store2 = ConvenienceStoreInfo(storename="경상관 CU", storerow=16, storecol=17)
    store3 = ConvenienceStoreInfo(storename="수원대학교 CU")
    db.session.add(store1)
    db.session.add(store2)
    db.session.add(store3)

    coordinates = [(5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10)]
    for x, y in coordinates:    # 1
        map_entry = ConvenienceStoreMap(storeinfoid=2, storex=x, storey=y, storestate=1)
        db.session.add(map_entry)
    coordinates = [(9,0), (10,0), (11,0), (12,0), (13,0), (14,0), (15,0)]
    for x, y in coordinates:    # 2
        map_entry = ConvenienceStoreMap(storeinfoid=2, storex=x, storey=y, storestate=2)
        db.session.add(map_entry)
    coordinates = [(6,3), (8,3), (6,4), (8,4), (6,5), (8,5), (6,6), (8,6), (6,7), (8,7), (6,8), (8,8), (6,9), (8,9), (6,10), (8,10)]
    for x, y in coordinates:    # 3
        map_entry = ConvenienceStoreMap(storeinfoid=2, storex=x, storey=y, storestate=3)
        db.session.add(map_entry)
    coordinates = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (0,1), (0,2), (9,3), (11,3), (9,4), (11,4), (9,5), (11,5), (9,6), (9,7), (9,8), (9,9), (9,10), (4, 13), (5,13)]
    for x, y in coordinates:    # 4
        map_entry = ConvenienceStoreMap(storeinfoid=2, storex=x, storey=y, storestate=4)
        db.session.add(map_entry)
    coordinates = [(2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9), (2,10)]
    for x, y in coordinates:    # 5
        map_entry = ConvenienceStoreMap(storeinfoid=2, storex=x, storey=y, storestate=5)
        db.session.add(map_entry)
    coordinates = [(1,16), (2,16), (3,16)]
    for x, y in coordinates:    # 6
        map_entry = ConvenienceStoreMap(storeinfoid=2, storex=x, storey=y, storestate=6)
        db.session.add(map_entry)
    coordinates = [(11,7), (11,8), (11,9)]
    for x, y in coordinates:    # 7
        map_entry = ConvenienceStoreMap(storeinfoid=2, storex=x, storey=y, storestate=7)
        db.session.add(map_entry)
    coordinates = []
    for x, y in coordinates:    # 8
        map_entry = ConvenienceStoreMap(storeinfoid=2, storex=x, storey=y, storestate=8)
        db.session.add(map_entry)
    
    

    
    db.session.commit()

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
