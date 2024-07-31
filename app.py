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
        
    return app

def insert_dummy_data():
    from db_model.mysql import ConvenienceStoreInfo, ConvenienceStoreMap
    
    # 더미 데이터 생성
    store1 = ConvenienceStoreInfo(storename="미래혁신관 CU")
    store2 = ConvenienceStoreInfo(storename="경상관 CU")
    store3 = ConvenienceStoreInfo(storename="수원대학교 CU")
    
    
    db.session.add(store1)
    db.session.add(store2)
    db.session.add(store3)
    
    db.session.commit()

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
