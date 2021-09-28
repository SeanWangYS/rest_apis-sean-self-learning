import sqlite3
from sqlite3.dbapi2 import connect
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True, 
        help='This field connot be left blank!'
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name, ))
        row  = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if __class__.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}, 400
        
        data = __class__.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            __class__.insert(item)
        except:
            return {"message": "An error occurred inserting the"}, 500 # Internal Sever Error

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(slef, name):
        if __class__.find_by_name(name):
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

        item = __class__.find_by_name(name)
        updated_item = {"name": name, "price": data['price']}

        if item:
            try:
                __class__.update_item(updated_item)
            except:
                return {"message": "An error occurred updating the item"}, 500
        else:
            try:
                __class__.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item"}, 500
        return updated_item, 201
 
    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        items = [{'name':row[0], 'pirce':row[1]} for row in result]

        connection.close()

        return {'items': items}

