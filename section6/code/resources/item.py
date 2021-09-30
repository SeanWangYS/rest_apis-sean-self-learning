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
    parser.add_argument('store_id', 
        type=int, 
        required=True, 
        help='Every item needs a store id.'
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

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting: {str(e)}"}, 500 # Internal Sever Error

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': "Item deleted"}
        return {'message': 'Item not found.'}, 404
        

        
    def put(self, name):
        data = __class__.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # return {'items': [item.json() for item in ItemModel.query.all()]}  # 個人觀點，MVC架構裡，model的元件，不應該寫在controller
        return {'items': list(map(lambda x :x.json(), ItemModel.query.all()))} # 這種寫法，寫Rudy, Java的工程師將容易理解，假如是在多語言開發的專案，用這種寫法，可以有跟其他語言的一致性 
        

