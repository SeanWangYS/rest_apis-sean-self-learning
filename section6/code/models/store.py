from db import db

class StoreModel(db.Model):   #db.Model→it's going to create that mapping between the database and this entity
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') 
    # 會自動去ItemModel找尋是何種關係，然後就發現原來在ItemModel 有註冊一個指向 stores table 的 foreign key, 且返回 items, it is a list of ItemModel
    # 預設每次建立StoreModel物件，都會生成 items 物件，太耗費成本，所以用lazy='dynamic' 關掉該功能
    
    def __init__(self, name):
        self.name  = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}
        # when we use lazy='dynamic'，items is not longer a list of ItemModel, now it is a query builder that has the ability to look into the items table

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()