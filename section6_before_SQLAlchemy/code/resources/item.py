import sqlite3
from sqlite3.dbapi2 import connect
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True, 
        help='This field connot be left blank!'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)  # item here is a class object
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}, 400
        
        data = __class__.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the"}, 500 # Internal Sever Error

        return item.json(), 201

    def delete(self, name):
        if ItemModel.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name, ))

            connection.commit()
            connection.close()

            return {'message': 'Item deleted'}
        return {'message': "Item doesn't exist"}, 400
        
    def put(self, name):
        data = __class__.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item:
            try:
                updated_item.update()   # 假如有找到，理應是對 item 物件做update呀, 這裡變數的使用上邏輯有誤（但實際上沒問題），講師說之後會修正
            except:
                return {"message": "An error occurred updating the item"}, 500
        else:
            try:
                updated_item.insert()  # 假若找不到item, 就建立新的updated_item,並且insert
            except:
                return {"message": "An error occurred inserting the item"}, 500
        return updated_item.json()
 

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        
        items = [{'name':row[0], 'pirce':row[1]} for row in result]

        connection.close()

        return {'items': items}

