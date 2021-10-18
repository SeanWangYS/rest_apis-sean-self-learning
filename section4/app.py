from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)  # api works with resources and every resources has to be a class 

jwt = JWT(app, authenticate, identity) # JWT create a new endpoint "/auth", JW token would be sent to client after passing authetication

items = []


class Item(Resource):  # 因為搭配了Api(), 每個Resource 我們可以get, post, delete, put, 不用特別指定路徑以及 http verb
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True, 
        help='This field connot be left blank!'
    )

    @jwt_required()
    def get(self, name):    # retrive an item
        item = next(filter(lambda x: x['name']==name , items), None)  # next(<iterator>)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):   # create an item 
        if next(filter(lambda x: x['name']==name , items), None) is not None:
            return {'message': f'An item with name {name} already exists.'}, 400
        
        data = __class__.parser.parse_args()
        # data = request.get_json(silent=True)         # force=True 就算browser content-type 沒有設定，依然將body的內容以json 解析, 但無法解析時，則會觸發 error,  # silence=True 用意與前面相同，但無法解析時，只會回傳None
        
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(slef, name):
        global items
        items = list(filter(lambda x: x['name']!=name, items))
        return {'message': 'Item deleted'}
        
    def put(self, name):
        data = __class__.parser.parse_args() # receive json pay load
    
        # data = request.get_json()  # 這個做法是接收整個json payload, 但josn payload 內有額外的key value pair時，也會被update 進去，這就不是我要的

        item = next(filter(lambda x: x['name']==name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data) # item is a dictionary, 內建有 update() 
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
