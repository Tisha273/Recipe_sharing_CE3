from flask import Flask, jsonify, request

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Sample data
items = [
    {"id": 1, "name": "Chicken Biryani", "description": "Aromatic Indian rice dish"},
    {"id": 2, "name": "Paneer Butter Masala", "description": "Creamy curry"},
    {"id": 3, "name": "Grilled Chicken", "description": "Healthy grilled dish"},
    {"id": 4, "name": "Veg Pulao", "description": "Rice with veggies"},
]

# Dummy data for the mymodel endpoint
mymodel_data = [
    {'id': 1, 'name': 'Recipe1', 'ingredients': 'Eggs, Flour, Milk'},
    {'id': 2, 'name': 'Recipe2', 'ingredients': 'Rice, Chicken, Soy Sauce'}
]

@app.route('/')
def home():
    return "Flask is working!"

# Search route
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    results = [item for item in items if query in item['name'].lower()]  # Case-insensitive search
    return jsonify(results)

# API endpoints for mymodel (GET, POST, PUT, DELETE)
@app.route('/api/mymodel', methods=['GET'])
def get_mymodels():
    return jsonify(mymodel_data), 200

@app.route('/api/mymodel/<int:id>', methods=['GET'])
def get_mymodel(id):
    item = next((item for item in mymodel_data if item['id'] == id), None)
    if item:
        return jsonify(item), 200
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/api/mymodel', methods=['POST'])
def create_mymodel():
    new_item = request.get_json()
    mymodel_data.append(new_item)
    return jsonify(new_item), 201

@app.route('/api/mymodel/<int:id>', methods=['PUT'])
def update_mymodel(id):
    item = next((item for item in mymodel_data if item['id'] == id), None)
    if item:
        updated_data = request.get_json()
        item.update(updated_data)
        return jsonify(item), 200
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/api/mymodel/<int:id>', methods=['DELETE'])
def delete_mymodel(id):
    global mymodel_data
    mymodel_data = [item for item in mymodel_data if item['id'] != id]
    return jsonify({'message': 'Item deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)