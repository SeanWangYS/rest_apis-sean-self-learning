from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # SQLAlchemy 本身就有這個功能，所以關掉Flask的相同功能
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tebles():
    db.create_all() # this will create file data.db at 'sqlite:///data.db', and it's gonna create all of the tables in the file unless it exist already (也太神奇了)
    # 能夠建立table 的前提，是import Resource 元件，Resource 元件內又import Model元件，Model元件內有關於table的資訊描述

jwt = JWT(app, authenticate, identity) # /auth 路徑自動生成了


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')



if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
    