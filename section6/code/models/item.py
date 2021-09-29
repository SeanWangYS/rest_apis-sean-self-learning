from db import db

class ItemModel(db.Model):   #db.Model→it's going to create that mapping between the database and this entity
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))             # 建立物件時，會直接把這個variable丟入 __init__ 建構子
    price = db.Column(db.Float(precision=2))
    
    def __init__(self, name, price):
        self.name  = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=? LIMIT 1 # 返回的是一個ItemModel物件


    def save_to_db(self):
        db.session.add(self) # The session in this instance is a collection of objects, that we're going to write to the database.
        db.session.commit()
        # SQLAlchemy will do an update instead of an insert.So this method here actually is useful for both the update and the insert.
        

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()