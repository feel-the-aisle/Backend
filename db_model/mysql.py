from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ConvenienceStoreInfo(db.Model):
    __tablename__ = 'ConvenienceStoreInfo'
    
    id = db.Column(db.Integer, primary_key=True)
    storename = db.Column(db.String(32))
    storerow = db.Column(db.Integer)
    storecol = db.Column(db.Integer)
    
    # 관계 설정
    maps = db.relationship('ConvenienceStoreMap', backref='store_info', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'storename': self.storename,
            'storerow': self.storerow,
            'storecol': self.storecol,
            'maps': [map.to_dict() for map in self.maps]
        }
    def to_id(self):
        return {
            'id': self.id,
            'storename': self.storename
        }

class ConvenienceStoreMap(db.Model):
    __tablename__ = 'ConvenienceStoreMap'
    
    id = db.Column(db.Integer, primary_key=True)
    storeinfoid = db.Column(db.Integer, db.ForeignKey('ConvenienceStoreInfo.id'), nullable=False)
    storex = db.Column(db.Integer)
    storey = db.Column(db.Integer)
    storestate = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'storeinfoid': self.storeinfoid,
            'storex': self.storex,
            'storey': self.storey,
            'storestate': self.storestate,
        }