from flask import Flask, jsonify, request, render_template

app = Flask(__name__) # __name__ 會給 Flask 物件一個 unique name, 先知道這樣就好

stores = [
    {
        'name': 'My Wonderful Store', 
        'items': [
            {
                'name': 'My Item', 
                'price': 15.99
            }
        ]
    }
]


@app.route('/')
def home():
    return render_template('index.html')


# we are a server not browser in this scirpt
# POST - used to receive data, at server's perspective 
# GET - used to send data back only, at server's perspective 

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name): 
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})
    

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name): 
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'], 
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})



# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name): 
    for store in stores:
        if store['name'] == name:
            items = store['items']
            return jsonify({'items': items})
    return jsonify({'message': 'store not found'})


app.run(port=5000) # can tell it a specific port