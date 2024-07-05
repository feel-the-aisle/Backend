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
        # 각 기능의 엔드포인트 위치
        # url_prefix는 엔드포인트 앞에 붙는 경로임
        from detect_products.view.detect_view import detect_bp
        app.register_blueprint(detect_bp, url_prefix='/detect-products')
        
        #app.register_blueprint(find_view.feel_the_aisle, url_prefix='/find-path')
        #app.register_blueprint(search_view.feel_the_aisle, url_prefix='/search-recipes')        
    return app
        

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
